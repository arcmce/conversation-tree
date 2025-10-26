from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate, ConversationOut

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/", response_model=ConversationOut)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    conv = Conversation(title=payload.title)
    db.add(conv)
    db.commit()
    db.refresh(conv)

    return conv
    