from pydantic import BaseModel, Field
from typing import List

class CommunityModel(BaseModel):
    id: int = Field(..., description="Community ID")
    members: List[str] = Field(..., description="List of member IDs")
    size: int = Field(..., description="Number of members in the community")
    density: float = Field(..., description="Density of the community")
    suspicion_score: float = Field(..., description="Suspicion score of the community")