from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
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

@router.get("/", response_model=List[ConversationOut], response_model_exclude_none=True)
def list_conversations(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    include_summary: bool = Query(False)
):
    q = select(Conversation).order_by(Conversation.created_at.desc()).offset(offset).limit(limit)
    rows = db.execute(q).scalars().all()

    if include_summary:
        return rows

    out = []
    for c in rows:
        data = ConversationOut.model_validate(c).model_dump()
        data["summary"] = None
        out.append(data)

    return out