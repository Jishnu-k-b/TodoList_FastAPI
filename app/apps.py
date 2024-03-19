from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId

from .models import Todo

app = FastAPI()

# MongoDb connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todo"]


# Create todo
@app.post("/todos/")
async def create_todo(todo: Todo):
    todo_dict = todo.model_dump()
    inserted_id = collection.insert_one(todo_dict).inserted_id

    todo_dict["_id"] = str(inserted_id)

    return todo_dict
