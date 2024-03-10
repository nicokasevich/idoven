from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import get_access_token, get_current_user, get_password_hash
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.security import Token
from app.schemas.user import UserItem, UserRegister

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repository: UserRepository = Depends(),
):
    return get_access_token(form_data, user_repository)


@router.post("/register", response_model=UserItem)
def register(
    request: UserRegister,
    current_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if user_repository.get_by_username(request.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    if user_repository.get_by_email(request.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    request.password = get_password_hash(request.password)

    return user_repository.create(request)


@router.get("/me", response_model=UserItem)
def me(current_user: User = Depends(get_current_user)):
    return current_user
