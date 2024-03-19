from fastapi import FastAPI
from .routers import todo_router, auth_router

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(todo_router.router)
