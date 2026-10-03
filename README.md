# 🌿 Greenhouse-Agent: AI-Powered Autonomous Agronomist & Automation Engine

**Greenhouse-Agent** is an intelligent greenhouse automation backend built with **FastAPI**, **LangGraph**, and **Google Gemini 3.5 Flash Vision**.

The engine processes real-time sensor measurements (temperature, soil moisture, light levels), performs visual crop disease diagnostics using computer vision, integrates real-time weather context (via the Open-Meteo API), and returns validated structured JSON designed for desktop and IoT client interfaces (such as C# WPF applications).

---

## ✨ Key Features

- **🔍 Vision Diagnostic Engine:** Uses Gemini 3.5 Flash Vision to detect plant diseases, pest damage, and nutrient deficiencies directly from uploaded leaf images.
- **🌡️ Sensor Analytics & Structured Output:** Evaluates ambient sensor metrics and returns strictly validated `GreenhouseReport` schemas via Pydantic (`/analyze`).
- **⛅ Dynamic Weather Context:** Integrates the Open-Meteo Forecast & Geocoding APIs to tailor ventilation and climate recommendations to local outdoor conditions.
- **💬 Conversational AI Assistant:** Stateful agronomic chat (`/chat`, powered by LangGraph `MemorySaver`) that maintains multi-turn context per session thread.
- **⚡ Production-Ready FastAPI:** CORS configuration, automatic temporary file lifecycle management (`temp_uploads/`), and token-optimized prompt design.
- **🖥️ Desktop Client Ready:** Designed for integration with C# WPF desktop apps via asynchronous REST endpoints.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **AI Orchestration & Memory:** LangChain, LangGraph (`MemorySaver`)
- **LLM & Vision Model:** Google Gemini 3.5 Flash (`ChatGoogleGenerativeAI`)
- **Data Validation:** Pydantic v2
- **External Services:** Open-Meteo API (Geocoding & Weather Forecasts)
- **Configuration:** `python-dotenv`

---

## 📁 Project Structure

```text
Greenhouse-Agent/
├── services/
│   └── weather_service.py   # Open-Meteo API integration (weather & geocoding)
├── models.py                # Pydantic schemas (GreenhouseReport, SystemCommand, etc.)
├── agent.py                 # LangGraph agent orchestration, tools, and session memory
├── tools.py                 # Gemini Vision diagnostic utilities
├── app.py                   # FastAPI endpoints (/analyze, /chat, /health)
├── .env                     # GOOGLE_API_KEY environment configuration
└── requirements.txt         # Dependencies
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/MateNozadze/Greenhouse-Agent.git
cd Greenhouse-Agent
```

### 2. Create and Activate a Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your Google Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Run the Server

```bash
uvicorn app:app --reload
```

- **Base URL:** http://127.0.0.1:8000
- **Interactive API Docs (Swagger UI):** http://127.0.0.1:8000/docs

---

## 📡 API Endpoints

### `POST /analyze`

Accepts multipart form data with sensor parameters and an optional crop image. Returns structured agronomic feedback and action directives.

**Content-Type:** `multipart/form-data`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `temperature` | float | yes | Current temperature (°C) |
| `soil_moisture` | float | yes | Current soil moisture (%) |
| `light_level` | float | yes | Ambient light level (lux) |
| `plant_type` | string | yes | Target crop species (e.g., `"Tomato"`) |
| `file` | file | no | Leaf image for vision diagnosis |
| `city` | string | no | City name for outdoor weather lookup |
| `latitude` / `longitude` | float | no | Coordinates for precise weather lookup |

### `POST /chat`

Contextual conversational endpoint for interactive AI assistance.

**Content-Type:** `application/json`

```json
{
  "message": "What is the optimal humidity for growing tomatoes?",
  "thread_id": "session_123"
}
```

### `GET /health`

System status check.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
