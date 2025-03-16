from app.schemas.user_base import UserBase

class UserCreate(UserBase):
    password: str