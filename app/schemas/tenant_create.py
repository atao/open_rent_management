from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class TenantCreate(BaseModel):
    firstname: str
    surname: str
    description: Optional[str] = None
    date_of_birth: datetime
    email: EmailStr
    phone: str
    address_id: Optional[int] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True