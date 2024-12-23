from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from models.task import Task
from datetime import datetime
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_tasks(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.created_date.desc()).all()
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})

@router.get("/task/create")
async def create_task_form(request: Request):
    return templates.TemplateResponse("task_form.html", {"request": request, "task": None})

@router.post("/task/create")
async def create_task(
        request: Request,
        name: str = Form(...),
        due_date: str = Form(None),
        lead_time: str = Form(None),
        db: Session = Depends(get_db)
):
    task = Task(
        name=name,
        due_date=datetime.fromisoformat(due_date) if due_date else None,
        lead_time=datetime.strptime(lead_time, "%H:%M").time() if lead_time else None,
        slug=str(uuid.uuid4())
    )
    db.add(task)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/task/{task_id}/edit")
async def edit_task_form(
        request: Request,
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return templates.TemplateResponse("task_form.html", {"request": request, "task": task})

@router.post("/task/{task_id}/edit")
async def edit_task(
        request: Request,
        task_id: int,
        name: str = Form(...),
        due_date: str = Form(None),
        lead_time: str = Form(None),
        check_mark: bool = Form(False),
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.name = name
    task.due_date = datetime.fromisoformat(due_date) if due_date else None
    task.lead_time = datetime.strptime(lead_time, "%H:%M").time() if lead_time else None
    task.check_mark = check_mark

    db.commit()
    return RedirectResponse(url="/", status_code=303)