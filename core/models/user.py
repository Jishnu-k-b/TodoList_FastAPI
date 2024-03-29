from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    _id: str
