from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.task import Task
from models.subtask import Subtask
from schemas import *
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/task', tags=['task'])

@router.get("/all_tasks", response_model=list[TaskResponse])
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task)).scalars().all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found.")
    return tasks

@router.post("/create_task", response_model=TaskResponse)
async def create_task(db: Annotated[Session, Depends(get_db)], creating_task: CreateTask):
    item = db.execute(insert(Task).values(
        name=creating_task.name,
        due_date=creating_task.due_date,
        lead_time=creating_task.lead_time,
        check_mark=creating_task.check_mark,
        slug=slugify(creating_task.name)
    ))
    db.commit()
    db.refresh(item)
    return item

@router.put("/update_task", response_model=TaskResponse)
async def update_task(request: Request, db: Annotated[Session, Depends(get_db)], task_id: int, updating_task: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found.")
    db.execute(update(Task).where(Task.id == task_id).values(
        name=updating_task.name,
        due_date=updating_task.due_date,
        lead_time=updating_task.lead_time,
        check_mark=updating_task.check_mark,
    ))
    db.commit()
    db.refresh(task)
    # return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
    return task

@router.put("/delete_task", response_model=StatusResponse)
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found.")
    db.execute(delete(Task).where(Task.id == task_id))
    db.execute(delete(Subtask).where(Subtask.task_id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}

