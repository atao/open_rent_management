from pydantic import BaseModel
from typing import Optional


class PropertyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address_id: Optional[int] = None
    property_manager_id: int

    class Config:
        orm_mode = True
