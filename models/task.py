from backend.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Time, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    name = Column(String)
    due_date = Column(DateTime)
    lead_time = Column(Time)
    check_mark = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)
    subtasks = relationship('Subtask', back_populates='task')