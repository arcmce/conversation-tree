from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ConversationCreate(BaseModel):
    title: str

class ConversationOut(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
