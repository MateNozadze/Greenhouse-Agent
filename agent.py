import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool

from tools import run_disease_analysis
from services.weather_service import fetch_weather_forecast
from models import GreenhouseReport

# 1. LLM მოდელის ინიციალიზაცია
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
    max_retries=5
)

# 2. Disease Analysis Tool
@tool
def analyze_plant_disease(image_path: str, plant_type: str = "unknown") -> dict:
    """Carefully analyzes a plant image to identify diseases using Vision AI."""
    return run_disease_analysis(image_path=image_path, vision_llm=llm, plant_type=plant_type)

# 3. Weather Forecast Tool
@tool
def get_outside_weather(latitude: float = 41.7151, longitude: float = 44.8271) -> dict:
    """Fetches real-time outside weather conditions (temperature, wind, etc.) to optimize greenhouse ventilation."""
    return fetch_weather_forecast(latitude=latitude, longitude=longitude)

tools = [analyze_plant_disease, get_outside_weather]

SYSTEM_PROMPT = """You are an expert Greenhouse AI Agronomist and Automation Engine.
Your job is to analyze sensor data, plant image analysis, and ambient weather conditions to evaluate overall greenhouse health.

Rules:
1. If an image path is provided, ALWAYS call `analyze_plant_disease`.
2. When making ventilation decisions, optionally check outside weather using `get_outside_weather`.
3. Provide optimal automation commands (fan, heater, irrigation, lighting) and clear recommendations in Georgian for the user.
"""

memory = MemorySaver()

# აგენტი დიაგნოსტიკისთვის
plant_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT,
    response_format=GreenhouseReport,
    checkpointer=memory
)

# აგენტი ჩატისთვის (თავისუფალი ტექსტური დიალოგისთვის)
chat_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="You are a helpful Greenhouse AI Assistant. Answer agronomy, weather, and plant care questions clearly and concisely in Georgian.",
    checkpointer=memory
)