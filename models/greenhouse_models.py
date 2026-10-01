from pydantic import BaseModel, Field
from typing import List, Optional, Any

class SystemCommand(BaseModel):
    device: str = Field(description="Target device name, e.g., 'fan', 'irrigation', 'light'")
    action: str = Field(description="Action to perform, e.g., 'on', 'off', 'set_target'")
    value: Optional[Any] = Field(default=None, description="Optional parameter value")

class GreenhouseReport(BaseModel):
    status: str = Field(description="Status: 'GOOD', 'WARNING', 'CRITICAL', or 'ERROR'")
    temperature: float = Field(description="Temperature in Celsius")
    soil_moisture: float = Field(description="Soil moisture percentage (0-100%)")
    light_level: float = Field(description="Light level intensity (0-1024)")
    
    disease_name: Optional[str] = Field(default=None, description="Disease name or 'Healthy'")
    confidence: str = Field(default="low", description="Confidence level: 'high', 'medium', 'low'")
    
    issues: List[str] = Field(default_factory=list, description="List of identified issues")
    action_plan: List[str] = Field(default_factory=list, description="Recommended action steps")
    commands: List[SystemCommand] = Field(default_factory=list, description="Automation commands for C#")