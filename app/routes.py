from fastapi import HTTPException, APIRouter
from pymongo import MongoClient
from bson import ObjectId

from .models import Todo


router = APIRouter()

# MongoDb connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todo"]


# Create todo
@router.post("/todos/")
async def create_todo(todo: Todo):
    todo_dict = todo.model_dump()
    inserted_id = collection.insert_one(todo_dict).inserted_id

    todo_dict["_id"] = str(inserted_id)

    return todo_dict


# Read all todo
@router.get("/todos/")
async def read_all_todos():
    todos = []
    for todo in collection.find():
        todo["_id"] = str(todo["_id"])
        todos.append(todo)
    return todos


# Read a todo
@router.get("/todos/{todo_id}")
async def read_todo(todo_id: str):
    todo = collection.find_one({"_id": ObjectId(todo_id)})
    if todo:
        todo["_id"] = str(todo["_id"])
        return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# Update a todo
@router.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo: Todo):
    todo_dict = todo.model_dump()
    updated_todo = collection.update_one(
        {"_id": ObjectId(todo_id)}, {"$set": todo_dict}
    )
    if updated_todo.modified_count:
        return {"message": "Todo updated successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")


# Delete a todo
@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    deleted_todo = collection.delete_one({"_id": ObjectId(todo_id)})
    if deleted_todo.deleted_count:
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")
