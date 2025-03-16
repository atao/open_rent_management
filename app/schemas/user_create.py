from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None