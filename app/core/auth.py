from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.user import User
from app.services.authentication_service import AuthenticationService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def get_auth_service(db: Session = Depends(get_db)):
    return AuthenticationService(oauth2_scheme, db)


def get_current_active_user(
    token: str = Depends(oauth2_scheme), auth_service: AuthenticationService = Depends(get_auth_service)
) -> User:
    return auth_service.get_current_active_user(token)
