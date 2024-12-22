from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from fastapi import status, Response

class TaskBase(BaseModel):
    name: str
    due_date: Optional[datetime] = None
    lead_time: Optional[time] = None
    check_mark: Optional[bool] = False

class CreateTask(TaskBase):
    pass

class UpdateTask(TaskBase):
    pass

class SubtaskBase(BaseModel):
    name: str
    due_date: Optional[datetime] = None
    lead_time: Optional[time] = None
    check_mark: Optional[bool] = False

class CreateSubtask(SubtaskBase):
    pass

class UpdateSubtask(SubtaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_date: datetime
    slug: str

    class Config:
        from_attributes = True

class SubtaskResponse(SubtaskBase):
    id: int
    task_id: int
    slug: str

    class Config:
        from_attributes = True

class StatusResponse(BaseModel):
    # Response(status.HTTP_200_OK)
    pass
