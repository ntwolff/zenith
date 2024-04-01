from pydantic import BaseModel
from typing import List

class Community(BaseModel):
    community_id: int
    members: List[str]
    size: int
    density: float
    suspicion_score: float