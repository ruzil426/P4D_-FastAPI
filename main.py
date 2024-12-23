from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from routers import task, subtask
from starlette.staticfiles import StaticFiles

app = FastAPI(title="Todo List API")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(task.router)
app.include_router(subtask.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)