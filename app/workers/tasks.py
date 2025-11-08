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
def recluster_conversation(self, conversation_id: int, threshold: float = 0.66):
    db: Session = SessionLocal()
    try:
        rows = db.execute(
            select(Turn.id, Turn.role, Turn.content, Turn.embedding).where(
                Turn.conversation_id == conversation_id, Turn.embedding.is_not(None))
                .order_by(Turn.id)
        ).all()
        if not rows:
            return {"clusters": 0}

        # ids = [t.id for t in turns]

        def _unit(v):
            v = np.asarray(v, dtype=np.float32)
            n = np.linalg.norm(v)
            return v / (n + 1e-12)

        segments = []
        i = 0
        while i < len(rows):
            tid, role, content, emb = rows[i]
            if role == "user" and i + 1 < len(rows):
                tid2, role2, content2, emb2 = rows[i + 1]
                if role2 == "assistant":
                    seg_vec = _unit((0.3*_unit(emb) + 0.7*_unit(emb2)) / 2.0)
                    segments.append((
                        [tid, tid2],
                        seg_vec,
                        f"Q: {content}\nA: {content2}"
                    ))
                    i += 2
                    continue
            seg_vec = _unit(emb)
            segments.append(([tid], seg_vec, content))
            i += 1


        # vecs = [_unit(np.array(t.embedding, dtype=np.float32)) for t in turns]
        seg_vecs = [s[1] for s in segments]

        remaining = set(range(len(segments)))
        clusters_idx = []

        while remaining:
            seed = min(remaining)
            remaining.remove(seed)
            cluster = [seed]
            centroid = seg_vecs[seed]
            changed = True
            while changed:
                changed = False
                to_add = []
                for j in list(remaining):
                    if float(np.dot(seg_vecs[j], centroid)) >= threshold:
                        to_add.append(j)
                if to_add:
                    for j in to_add:
                        remaining.remove(j)
                    cluster.extend(to_add)
                    mat = np.stack([seg_vecs[i] for i in cluster])
                    centroid = _unit(mat.mean(axis=0))
                    changed = True
            clusters_idx.append(cluster)

        db.query(Cluster).filter(Cluster.conversation_id == conversation_id).delete()
        db.commit()

        created = 0
        for seg_group in clusters_idx:
            c = Cluster(conversation_id=conversation_id)
            db.add(c); db.flush()
            mat = np.stack([seg_vecs[k] for k in seg_group])
            centroid = _unit(mat.mean(axis=0))
            for k in seg_group:
                turn_ids, seg_vec, _txt = segments[k]

                score = float(np.dot(seg_vec, centroid))
                db.add(ClusterMember(cluster_id=c.id, turn_id=tid, score=score))
            created += 1
        db.commit()
        return {"clusters": created}

    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.add")
def add(x, y):
    return x + y