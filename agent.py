import sys
import os

# პროექტის Root საქაღალდის ცნობა Python-ისთვის
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool

# ახლა იმპორტი სუფთად იმუშავებს `tools` პაკეტიდან:
from tools import run_disease_analysis

# 1. AI მოდელის ერთადერთი ინსტანცია მთელ აპლიკაციაში
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    max_retries=5
)

# 2. Tool-ის რეგისტრაცია ცენტრალური LLM-ის გადაცემით
@tool
def analyze_plant_disease(image_path: str, plant_type: str = "unknown") -> dict:
    """Carefully analyzes a plant image to identify diseases using the central Vision AI.

    Args:
        image_path: Local path to the image file (e.g., 'leaf.jpg').
        plant_type: Optional species/name of the plant if provided by user (e.g., 'Tomato', 'Cucumber'). Defaults to 'unknown'.
    """
    return run_disease_analysis(image_path=image_path, vision_llm=llm, plant_type=plant_type)

tools = [analyze_plant_disease]

SYSTEM_PROMPT = """You are a precise Greenhouse AI Assistant.
When asked to analyze a plant image or check for diseases, 
use the `analyze_plant_disease` tool with the provided image path.
"""

memory = MemorySaver()

plant_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=SYSTEM_PROMPT, 
    checkpointer=memory
)