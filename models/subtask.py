from backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from models.task import Task

class Subtask(Base):
    __tablename__ = "subtasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    due_date = Column(DateTime)
    lead_time = Column(Time)
    check_mark = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    slug = Column(String, unique=True, index=True)
    task = relationship('Task', back_populates='subtasks')