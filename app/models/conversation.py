from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    turns = relationship("Turn", back_populates="conversation", cascade="all, delete-orphan")
    clusters = relationship("Cluster", back_populates="conversation", cascade="all, delete-orphan")