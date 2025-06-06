from pydantic import BaseModel
from typing import Optional


class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
