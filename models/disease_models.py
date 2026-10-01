from pydantic import BaseModel, Field
from typing import Optional

class DiseaseAnalysisOutput(BaseModel):
    is_confident: bool = Field(
        description="True if the model is confident in the visual diagnosis based solely on the image quality and visible symptoms. False if the image is blurry, ambiguous, or the symptoms are not recognizable."
    )
    disease_name: Optional[str] = Field(
        default=None,
        description="The exact standard English name of the plant disease (e.g. 'Early Blight'). Must be None if is_confident is False or the plant is Healthy."
    )
    status_summary: str = Field(
        description="A brief description of what is seen. If is_confident is False, explain WHY (e.g. 'Image too blurry', 'Symptoms ambiguous'). If Healthy, state it."
    )