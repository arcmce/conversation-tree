from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200))
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    conversation = relationship("Conversation", back_populates="clusters")
    members = relationship("ClusterMember", back_populates="cluster", cascade="all, delete-orphan")


class ClusterMember(Base):
    __tablename__ = "cluster_members"
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id", ondelete="CASCADE"), nullable=False)
    turn_id = Column(Integer, ForeignKey("turns.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float)
    __table_args__ = (UniqueConstraint("cluster_id", "turn_id", name="uq_cluster_turn"),)

    cluster = relationship("Cluster", back_populates="members")
