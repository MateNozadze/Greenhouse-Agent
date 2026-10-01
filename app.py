import os
import uuid
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. იმპორტები შენი მოდულებიდან
from models import GreenhouseReport
from agent import plant_agent, chat_agent

# 2. FastAPI აპლიკაციის ინიციალიზაცია
app = FastAPI(
    title="Greenhouse AI Agent API",
    description="Backend API for C# WPF client delivering AI plant diagnostics & automation decisions",
    version="1.0"
)

# 3. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. დროებითი ფაილების საქაღალდე
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


# ==========================================
# 5. PYDANTIC MODEL-ები (ყოველთვის თავში!)
# ==========================================

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "default_session"


class ChatResponse(BaseModel):
    reply: str
    thread_id: str


# ==========================================
# 6. ENDPOINT-ები (ფუნქციები ბოლოში!)
# ==========================================

@app.get("/", tags=["Health"])
def read_root():
    return {"status": "Greenhouse AI Agent Backend is up and running!"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "Greenhouse-Agent"}


@app.post("/analyze", response_model=GreenhouseReport, tags=["Analysis"])
async def analyze_greenhouse(
    file: Optional[UploadFile] = File(None),
    temperature: float = Form(22.0),
    soil_moisture: float = Form(60.0),
    light_level: float = Form(500.0),
    plant_type: str = Form("unknown"),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    city: Optional[str] = Form("Tbilisi")
):
    temp_file_path = None
    try:
        if file and file.filename:
            allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
            file_extension = os.path.splitext(file.filename)[1].lower() or ".jpg"
            
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported file format '{file_extension}'. Allowed formats: {', '.join(allowed_extensions)}"
                )

            temp_file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}{file_extension}")
            contents = await file.read()
            with open(temp_file_path, "wb") as f:
                f.write(contents)

        user_prompt = (
            f"Analyze greenhouse current status:\n"
            f"- Temperature: {temperature}°C\n"
            f"- Soil Moisture: {soil_moisture}%\n"
            f"- Light Level: {light_level}\n"
            f"- Plant Species: {plant_type}\n"
        )
        if temp_file_path:
            user_prompt += f"- Image uploaded at path: '{temp_file_path}'"

        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        result = plant_agent.invoke(
            {"messages": [("user", user_prompt)]},
            config
        )

        structured_response = result.get("structured_response")
        if structured_response:
            return structured_response

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Agent executed but failed to return structured report JSON."
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis pipeline error: {str(e)}"
        )

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception:
                pass


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_greenhouse_ai(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        result = chat_agent.invoke(
            {"messages": [("user", request.message)]},
            config
        )
        
        raw_content = result["messages"][-1].content
        
        # Gemini API-ს მიერ დაბრუნებული ლისტიდან მხოლოდ ტექსტის ამოღება
        # (ცილდება ზედმეტი metadata/extras და იზოგება ტოკენები)
        if isinstance(raw_content, list):
            clean_reply = "".join(
                item["text"] for item in raw_content 
                if isinstance(item, dict) and "text" in item
            )
        else:
            clean_reply = str(raw_content)

        return ChatResponse(reply=clean_reply, thread_id=request.thread_id)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Chat pipeline error: {str(e)}"
        )