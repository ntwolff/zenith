from app.models.v2.base import AbstractBaseModel
from typing import List

class CommunityModel(AbstractBaseModel):
    community_id: int
    members: List[str]
    size: int
    density: float
    suspicion_score: float