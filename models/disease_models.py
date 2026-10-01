from pydantic import BaseModel, Field
from typing import Optional

class DiseaseAnalysisOutput(BaseModel):
    is_confident: bool = Field(
        description="True if Gemini is confident in the visual diagnosis. False if blurry or ambiguous."
    )
    disease_name: Optional[str] = Field(
        description="Exact standard English name of the disease (e.g. 'Early Blight'). None if not confident or Healthy."
    )
    status_summary: str = Field(
        description="Brief description of findings or reason for uncertainty."
    )