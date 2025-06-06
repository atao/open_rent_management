from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
import jwt
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.auth_errors import AuthError
from app.models.user import User
from app.schemas.token import RefreshToken, TokenData


class AuthenticationService:
    def __init__(
        self,
        oauth2_scheme: Annotated[OAuth2PasswordBearer, Depends],
        db: Annotated[Session, Depends],
    ):
        self.oauth2_scheme = oauth2_scheme
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_secret_key(self):
        if Settings.secret_key is None:
            raise ValueError("SECRET_KEY environment variable is not set")
        return Settings.secret_key

    def get_username_from_payload(self, token: str):
        if token is None:
            return None
        payload = jwt.decode(token, self.get_secret_key(), algorithms=[Settings.algorithm])
        if payload is None:
            return None
        return payload.get("sub")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate_user(self, email: str, password: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return False
        if user.disabled:
            raise Exception(AuthError.USER_DISABLED)
        if not self.verify_password(password, user.password):
            return False
        return user

    @staticmethod
    def is_password_secure(password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char in "!@#$%^&*()-+" for char in password):
            return False
        return True

    def login(self, email: str) -> RefreshToken:
        access_token = self.create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self.create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=Settings.REFRESH_TOKEN_EXPIRE_DAYS),
            refresh=True,
        )
        return RefreshToken(access_token=access_token, token_type="bearer", refresh_token=refresh_token)

    def create_access_token(
        self,
        data: dict[str, object],
        expires_delta: timedelta | None = None,
        refresh: bool = False,
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            if refresh:
                expire = datetime.now(timezone.utc) + timedelta(days=Settings.REFRESH_TOKEN_EXPIRE_DAYS)
            else:
                expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.get_secret_key(), algorithm=Settings.algorithm)
        return encoded_jwt

    def refresh_access_token(self, refresh_token: str) -> RefreshToken:
        try:
            username = self.get_username_from_payload(refresh_token)
            if username is None:
                raise Exception(AuthError.INVALID_REFRESH_TOKEN)
            user = self.db.query(User).filter(User.email == username).first()
            if user is None:
                raise Exception(AuthError.INVALID_REFRESH_TOKEN)
            access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
            return RefreshToken(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )
        except jwt.ExpiredSignatureError:
            raise Exception(AuthError.REFRESH_TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise Exception(AuthError.INVALID_REFRESH_TOKEN)

    def get_current_active_user(self, token: str) -> User:
        try:
            username = self.get_username_from_payload(token)
            if username is None:
                raise Exception(AuthError.COULD_NOT_VALIDATE_CREDENTIALS)
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise Exception(AuthError.COULD_NOT_VALIDATE_CREDENTIALS)
        user = self.db.query(User).filter(User.email == token_data.username).first()
        if user is None:
            raise Exception(AuthError.COULD_NOT_VALIDATE_CREDENTIALS)
        if user.disabled:
            raise Exception(AuthError.USER_DISABLED)
        return user
