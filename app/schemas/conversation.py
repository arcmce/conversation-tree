from pydantic import BaseModel, ConfigDict
from typing import Optional


class ConversationCreate(BaseModel):
    title: str

class ConversationOut(BaseModel):
    id: int
    title: str
    
    model_config = ConfigDict(from_attributes=True)
