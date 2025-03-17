from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.core.dependencies import get_db
from app.models.user import User
from app.schemas.token import RefreshToken, Token
from app.schemas.user_create import UserCreate
from app.schemas.user_response import UserResponse
from app.services.authentication_service import AuthenticationService
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

db = Depends(get_db)


def get_auth_service(db: Session = Depends(get_db)):
    return AuthenticationService(oauth2_scheme, db)


router = APIRouter()


@router.post("/token", response_model=RefreshToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> Token:
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.login(user.email)


@router.post("/refresh", response_model=RefreshToken)
async def refresh_access_token(
    refresh_token: str, auth_service: AuthenticationService = Depends(get_auth_service)
) -> RefreshToken:
    return auth_service.refresh_access_token(refresh_token)


@router.post("/register/")
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service),
) -> UserResponse:
    if user_in.email is None or user_in.password is None or user_in.password_confirm is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, password and password_confirm are required",
        )
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    is_password_secure = auth_service.is_password_secure(user_in.password)
    if not is_password_secure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit and one special character",
        )
    if user_in.password != user_in.password_confirm:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    hashed_password = auth_service.get_password_hash(user_in.password)
    user_data = user_in.model_dump(exclude={"password", "password_confirm"})
    user = User(**user_data, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.post("/logout/")
async def logout(refresh_token: str, auth_service: AuthenticationService = Depends(get_auth_service)):
    return HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Logout is not implemented")


@router.get("/users/me/")
async def read_users_me(
    current_user: User = Depends(get_auth_service().get_current_active_user),
):
    return current_user
