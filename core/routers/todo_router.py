from fastapi import HTTPException, APIRouter, Depends
from typing import Optional
from bson import ObjectId
from jose import jwt, JWTError

from ..models.todo import Todo
from ..database import db_conn
from ..auth.auth import oauth2_scheme
from ..config.config import SECRET_KEY, ALGORITHM

router = APIRouter()

collection = db_conn.get_todo_collection()


# Create todo for authenticated user
@router.post("/todos/")
async def create_todo(todo: Todo, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        todo_dict = todo.model_dump()
        todo_dict["owner"] = username
        inserted_id = collection.insert_one(todo_dict).inserted_id
        todo_dict["_id"] = str(inserted_id)
        return todo_dict
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Read all todo
@router.get("/todos/")
async def read_all_todos(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        todos = []
        for todo in collection.find({"owner": username}):
            todo["_id"] = str(todo["_id"])
            todos.append(todo)
        return todos
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Read a todo
@router.get("/todos/{todo_id}")
async def read_todo(
    todo_id: str,
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        todo = collection.find_one(
            {"_id": ObjectId(todo_id), "owner": username},
        )
        if todo:
            todo["_id"] = str(todo["_id"])
            return todo
        raise HTTPException(status_code=404, detail="Todo not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Update a todo for authenticated user
@router.put("/todos/{todo_id}")
async def update_todo(
    todo_id: str,
    todo_update: Todo,
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        todo_update_dict = todo_update.model_dump(exclude_unset=True)
        updated_todo = collection.update_one(
            {"_id": ObjectId(todo_id), "owner": username},
            {"$set": todo_update_dict},
        )
        if updated_todo.modified_count:
            return {"message": "Todo updated successfully"}
        raise HTTPException(status_code=404, detail="Todo not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Delete a todo for authenticated user
@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        deleted_todo = collection.delete_one(
            {"_id": ObjectId(todo_id), "owner": username}
        )
        if deleted_todo.deleted_count:
            return {"message": "Todo deleted successfully"}
        raise HTTPException(status_code=404, detail="Todo not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
