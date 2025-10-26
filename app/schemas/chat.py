from pydantic import BaseModel

class ChatRequest(BaseModel):
    content: str

class ChatResponse(BaseModel):
    assistant: str
    assistant_turn_id: int