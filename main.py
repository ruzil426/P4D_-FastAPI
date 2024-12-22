from fastapi import FastAPI, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.templating import Jinja2Templates
from routers import task, subtask
from sqlalchemy import select
from models.task import Task
from models.subtask import Subtask
from backend.db_depends import get_db
from fastapi.responses import JSONResponse, FileResponse
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


app = FastAPI(title="Todo List API")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(db: Annotated[Session, Depends(get_db)], request: Request):
    tasks = db.execute(select(Task)).scalars().all()
    subtasks = db.execute(select(Subtask)).scalars().all()

    return templates.TemplateResponse("index.html", {'request': request, 'tasks': tasks, 'subtasks': subtasks})

# @app.get('/update/{id}')
# async def update(id: int = None, db: Session = Depends(get_db)):
#     task.update_task(id)
#     url = app.url_path_for('root')
#     return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

app.include_router(task.router)
app.include_router(subtask.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)