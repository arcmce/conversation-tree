from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.cluster import Cluster, ClusterMember
from app.workers.tasks import recluster_conversation

router = APIRouter(prefix="/conversations", tags=["Tree"])

@router.post("/{conversation_id}/recluster")
def trigger_recluster(conversation_id, db: Session = Depends(get_db)):
    conv = db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    job = recluster_conversation.delay(conversation_id)

    return {"job_id": job.id}
