import base64
from langchain_core.messages import HumanMessage
from langchain_core.language_models import BaseChatModel
from models.disease_models import DiseaseAnalysisOutput
from services.wiki_service import fetch_wikipedia_summary

def run_disease_analysis(image_path: str, vision_llm: BaseChatModel, plant_type: str = "unknown") -> dict:
    """Core logic to analyze plant disease using injected LLM instance with optional plant context."""
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        structured_model = vision_llm.with_structured_output(DiseaseAnalysisOutput)

        # მცენარის კონტექსტის მომზადება
        plant_context = f" The user indicated this is a '{plant_type}'." if plant_type != "unknown" else ""

        system_instruction = (
            f"You are an expert, conservative Plant Pathologist AI.{plant_context}\n"
            "Analyze the image of the plant leaf very carefully.\n"
            "Your priority is to NEVER provide incorrect information.\n"
            "1. Pay close attention to visual lookalikes specific to this plant type "
            "(e.g., carefully differentiate Powdery Mildew from Late Blight, etc.).\n"
            "2. If blurry, poorly lit, or ambiguous, set is_confident=False.\n"
            "3. Only if highly confident, set is_confident=True and provide exact English name.\n"
            "4. If healthy, set is_confident=True, disease_name='None'."
        )

        message = HumanMessage(
            content=[
                {"type": "text", "text": system_instruction},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                }
            ]
        )

        analysis: DiseaseAnalysisOutput = structured_model.invoke([message])

        if not analysis.is_confident:
            return {
                "status": "UNCERTAIN",
                "message": f"AI cannot confirm diagnosis: {analysis.status_summary}. Please upload a clearer photo."
            }

        if analysis.disease_name is None or analysis.disease_name.lower() == "none":
            return {
                "status": "HEALTHY",
                "message": "The plant appears healthy.",
                "details": analysis.status_summary
            }

        wiki_info = fetch_wikipedia_summary(analysis.disease_name)
        return {
            "status": "DISEASE_DETECTED",
            "confirmed_disease": analysis.disease_name,
            "symptoms": analysis.status_summary,
            "wikipedia_summary": wiki_info
        }

    except FileNotFoundError:
        return {"error": f"Image file not found at path: {image_path}"}
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}