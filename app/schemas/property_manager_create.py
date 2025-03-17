from pydantic import BaseModel
from typing import Optional


class PropertyManagerCreate(BaseModel):
    firstname: str
    surname: str
    title: str
    email: str
    phone_number: Optional[str] = None
    address_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
