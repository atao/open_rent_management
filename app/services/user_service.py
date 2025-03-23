from fastapi import Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.models.auth_errors import AuthError
from app.models.user import User
from app.schemas.user_create import UserCreate
from app.schemas.user_response import UserResponse
from app.services.authentication_service import AuthenticationService


class UserService:
    def __init__(
        self,
        db: Annotated[Session, Depends],
        auth_service: Annotated[AuthenticationService, Depends],
    ):
        self.db = db
        self.auth_service = auth_service

    def register_user(self, user_in: UserCreate) -> UserResponse:
        if user_in.email is None or user_in.password is None or user_in.password_confirm is None:
            raise Exception(AuthError.EMAIL_PASSWORD_REQUIRED)
        if self.db.query(User).filter(User.email == user_in.email).first():
            raise Exception(AuthError.EMAIL_ALREADY_REGISTERED)
        if user_in.password != user_in.password_confirm:
            raise Exception(AuthError.PASSWORDS_DO_NOT_MATCH)
        is_password_secure = AuthenticationService.is_password_secure(user_in.password)
        if not is_password_secure:
            raise Exception(AuthError.PASSWORD_TOO_WEAK)
        hashed_password = self.auth_service.get_password_hash(user_in.password)
        user_data = user_in.model_dump(exclude={"password", "password_confirm"})
        user = User(**user_data, password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return UserResponse.model_validate(user)
