from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient
from typing import Optional
from bson import ObjectId
from datetime import timedelta
from jose import jwt, JWTError
from .models import Todo, User
from .auth import (
    pwd_context,
    users_collection,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    oauth2_scheme,
)

router = APIRouter()

# MongoDb connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todos"]


# User registration
@router.post("/register/", response_model=User)
async def register_user(user: User):
    user_dict = user.model_dump()
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    inserted_id = users_collection.insert_one(user_dict).inserted_id
    user_dict["_id"] = str(inserted_id)
    return user_dict


# User login
@router.post("/token/")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
