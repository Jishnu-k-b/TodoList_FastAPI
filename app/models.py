from pydantic import BaseModel, Field
from typing import Optional


class Todo(BaseModel):
    task_title: str = Field(default=None)
    task_description: str = Field(default=None)
    owner: Optional[str] = None


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    _id: str
