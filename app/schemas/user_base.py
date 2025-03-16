from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str
    disabled: Optional[bool] = None