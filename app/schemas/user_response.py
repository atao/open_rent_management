from datetime import datetime

from app.schemas.user_base import UserBase

class UserResponse(UserBase):

    id: int
    date_created: datetime
    date_updated: datetime

    class Config:
        orm_mode = True
        from_attributes = True