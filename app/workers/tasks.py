from app.workers.celery_app import celery_app
import numpy as np
from sqlalchemy.orm import Session, configure_mappers
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.turn import Turn
from app.models.cluster import Cluster, ClusterMember
from app.ai.embeddings import cosine_similarity
from app.db import base as models # noqa

configure_mappers()


@celery_app.task(bind=True, name="app.workers.tasks.recluster_conversation")
def recluster_conversation(self, conversation_id: int, threshold: float = 0.78):
    db: Session = SessionLocal()
    try:
        turns = db.execute(
            select(Turn.id, Turn.embedding).where(
                Turn.conversation_id == conversation_id, Turn.embedding.is_not(None))
        ).all()
        if not turns:
            return {"clusters": 0}

        ids = [t.id for t in turns]
        vecs = [np.array(t.embedding, dtype=np.float32) for t in turns]
        remaining = set(range(len(ids)))
        clusters = []

        while remaining:
            seed = remaining.pop()
            cluster = [seed]
            centroid = vecs[seed]
            changed = True
            while changed:
                changed = False
                to_add = []
                # for i in list(remaining)

    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.add")
def add(x, y):
    return x + y