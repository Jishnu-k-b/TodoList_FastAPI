from fastapi import FastAPI
from .routes import router as endpoints

app = FastAPI()

app.include_router(endpoints)
