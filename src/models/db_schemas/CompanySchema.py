from pydantic import BaseModel, Field
from datetime import datetime


class Company(BaseModel):
    Name: str = Field(..., description="Company name")
    CreatedAt: datetime = Field(default_factory=datetime.now)
    IsActive: bool = True
    