from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, APIRouter, Depends, status

from ..models.user import User
from ..database import db_conn
from ..config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..auth.auth import (
    pwd_context,
    authenticate_user,
    create_access_token,
)

router = APIRouter()
users_collection = db_conn.get_user_collection()


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
