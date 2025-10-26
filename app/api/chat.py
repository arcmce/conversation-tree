from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.turn import Turn
from app.ai.embeddings import embed_text
from app.ai.chat import generate_reply
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/conversations", tags=["Chat"])

@router.post("/{conversation_id}/chat", response_model=ChatResponse)
def chat(conversation_id: int, payload: ChatRequest, db: Session = Depends(get_db)):
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")

    uvec = embed_text(payload.content)
    user_turn = Turn(
        conversation_id=conversation_id,
        role="user",
        content=payload.content,
        embedding=uvec)
    db.add(user_turn)
    db.flush()

    msgs = [{"role": "system", "content": "You are a helpful assistant."}]
    for t in conv.turns:
        msgs.append({"role": t.role, "content": t.content})
    msgs.append({"role": "user", "content": payload.content})

    reply = generate_reply(msgs)
    avec = embed_text(reply)

    asst_turn = Turn(
        conversation_id=conversation_id,
        role="assistant",
        content=reply,
        embedding=avec)
    db.add(asst_turn)
    db.commit()
    db.refresh(asst_turn)

    return ChatResponse(assistant=reply, assistant_turn_id=asst_turn.id)
