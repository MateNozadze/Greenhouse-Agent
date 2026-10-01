from pydantic import BaseModel, Field
from typing import Optional

# 1. Vision Tool-ის სქემა (ეს აუცილებელია!)
class DiseaseAnalysisOutput(BaseModel):
    is_confident: bool = Field(
        description="True if Gemini is confident in the visual diagnosis based solely on the image quality and visible symptoms. False if the image is blurry, ambiguous, or the symptoms are not recognizable."
    )
    disease_name: Optional[str] = Field(
        description="The exact standard English name of the plant disease (e.g. 'Early Blight'). Must be None if is_confident is False or the plant is Healthy."
    )
    status_summary: str = Field(
        description="A brief description of what is seen. If is_confident is False, explain WHY (e.g. 'Image too blurry', 'Symptoms ambiguous'). If Healthy, state it."
    )

# 2. სათბურის რეპორტის სქემა
class GreenhouseReport(BaseModel):
    status: str = Field(description="Status: GOOD, WARNING, or CRITICAL")
    temperature: float = Field(description="Temperature in Celsius")
    soil_moisture: float = Field(description="Soil moisture percentage (0-100%)")
    light_level: float = Field(description="Light level intensity (0-1024)")
    issues: str = Field(description="Identified issues or 'None'")
    action_plan: str = Field(description="Recommended action for C# / user")