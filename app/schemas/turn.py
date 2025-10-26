from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class TurnCreate(BaseModel):
    role: str
    content: str

class TurnOut(BaseModel):
    id: int
    role: str
    content: str
    embedding: Optional[List[float]] = None
    
    model_config = ConfigDict(from_attributes=True)