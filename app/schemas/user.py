from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str


class UserItem(BaseModel):
    username: str
    full_name: str
    email: EmailStr
