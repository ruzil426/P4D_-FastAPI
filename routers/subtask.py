from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.task import Task
from models.subtask import Subtask
from schemas import *
from sqlalchemy import insert,select, update, delete
from slugify import slugify
# from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/subtask", tags=["subtask"])

@router.get("/all_subtasks", response_model=list[SubtaskResponse])
async def get_all_subtasks(db: Annotated[Session, Depends(get_db)]):
    subtasks = db.execute(select(Subtask)).scalars().all()
    if not subtasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtasks not found.")
    return subtasks

@router.post("/create_subtask", response_model=SubtaskResponse)
async def create_subtask(db: Annotated[Session, Depends(get_db)], task_id: int, creating_subtask: CreateSubtask):
    item = db.execute(insert(Subtask).values(
        name=creating_subtask.name,
        due_date=creating_subtask.due_date,
        lead_time=creating_subtask.lead_time,
        check_mark=creating_subtask.check_mark,
        slug=slugify(creating_subtask.name),
        task_id=task_id,
    ))
    db.commit()
    return item

@router.put("/update_subtask", response_model=SubtaskResponse)
async def update_subtask(db: Annotated[Session, Depends(get_db)], subtask_id: int, updating_subtask: UpdateSubtask):
    subtask = db.scalar(select(Task).where(Subtask.id == subtask_id))
    if subtask is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtasks not found.")
    db.execute(update(Subtask).where(Subtask.id == subtask_id).values(
        name=updating_subtask.name,
        due_date=updating_subtask.due_date,
        lead_time=updating_subtask.lead_time,
        check_mark=updating_subtask.check_mark,
    ))
    db.commit()
    return subtask

@router.put("/delete_subtask", response_model=SubtaskResponse)
async def delete_subtask(db: Annotated[Session, Depends(get_db)], subtask_id: int):
    subtask = db.scalar(select(Subtask).where(Subtask.id == subtask_id))
    if subtask is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtasks not found.")
    db.execute(delete(Subtask).where(Subtask.task_id == subtask_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Subtask delete is successful!'}