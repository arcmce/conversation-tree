from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.turn import Turn
from app.schemas.turn import TurnCreate, TurnOut
from app.ai.embeddings import embed_text, cosine_similarity

router = APIRouter(prefix="/conversations", tags=["Turns"])

@router.post("/{conversation_id}/turns", response_model=TurnOut)
def add_turn(conversation_id: int, payload: TurnCreate, db: Session = Depends(get_db)):
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    vec = embed_text(payload.content)
    turn = Turn(
        conversation_id=conversation_id, 
        role=payload.role, 
        content=payload.content, 
        embedding=vec)
    db.add(turn)
    db.commit()
    db.refresh(turn)

    return turn

@router.get("/{conversation_id}/turns", response_model=List[TurnOut])
def list_turns(conversation_id: int, db: Session = Depends(get_db)):
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    return conv.turns

@router.post("/{conversation_id}/ask")
def ask(
    conversation_id: int, 
    query: str = Query(..., description="User Question"), 
    top_k: int = Query(5, ge=1, le=50), 
    db: Session = Depends(get_db)
):
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    qvec = embed_text(query)
    scored = []
    for t in conv.turns:
        if t.embedding:
            scored.append((cosine_similarity(qvec, t.embedding), t))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [
        {
            "turn_id": t.id, 
            "role": t.role, 
            "content": t.content, 
            "score": round(s, 4)
        }
        for s, t in scored[:top_k]
    ]

    return {"matches": top}
