import faust
from typing import List

class CommunityModel(faust.Record):
    community_id: int
    members: List[str]
    size: int
    density: float
    suspicion_score: float