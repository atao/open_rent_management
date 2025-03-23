import datetime
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from app.models.auth_errors import AuthError
from app.models.user import User
from app.schemas.user_create import UserCreate
from app.services.user_service import UserService
from app.services.authentication_service import AuthenticationService


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def auth_service():
    return MagicMock(spec=AuthenticationService)


@pytest.fixture
def user_service(db_session, auth_service):
    return UserService(db=db_session, auth_service=auth_service)


def test_register_user_email_already_registered(user_service, db_session):
    user_in = UserCreate(full_name="test", email="test@example.com", password="password", password_confirm="password")
    db_session.query(User).filter().first.return_value = True
    with pytest.raises(Exception) as excinfo:
        user_service.register_user(user_in)
    assert str(excinfo.value) == AuthError.EMAIL_ALREADY_REGISTERED


@patch.object(AuthenticationService, "is_password_secure", return_value=False)
def test_register_user_password_too_weak(mock_is_password_secure, user_service, db_session):
    user_in = UserCreate(
        full_name="test", email="test@example.com", password="weakpassword", password_confirm="weakpassword"
    )
    db_session.query(User).filter().first.return_value = False
    with pytest.raises(Exception) as excinfo:
        user_service.register_user(user_in)
    assert str(excinfo.value) == AuthError.PASSWORD_TOO_WEAK


def test_register_user_passwords_do_not_match(user_service, db_session):
    user_in = UserCreate(
        full_name="test", email="test@example.com", password="password", password_confirm="differentpassword"
    )
    db_session.query(User).filter().first.return_value = False
    with pytest.raises(Exception) as excinfo:
        user_service.register_user(user_in)
    assert str(excinfo.value) == AuthError.PASSWORDS_DO_NOT_MATCH


@patch.object(AuthenticationService, "is_password_secure", return_value=True)
def test_register_user_success(mock_is_password_secure, user_service, db_session, auth_service):
    user_in = UserCreate(
        full_name="test", email="test@example.com", password="StrongPassword&123", password_confirm="StrongPassword&123"
    )
    auth_service.get_password_hash.return_value = "hashedpassword"
    db_session.query(User).filter().first.return_value = None

    user = User(
        id=1,
        email=user_in.email,
        full_name=user_in.full_name,
        password="hashedpassword",
        date_created=datetime.datetime.now(),
        date_updated=datetime.datetime.now(),
    )
    db_session.add.return_value = user
    db_session.commit.return_value = None

    def refresh_user(x):
        x.id = 1
        x.date_created = datetime.datetime.now()
        x.date_updated = datetime.datetime.now()
        return x

    db_session.refresh.side_effect = refresh_user

    user_response = user_service.register_user(user_in)

    assert user_response.email == user_in.email
    assert user_response.id == 1
    assert user_response.date_created is not None
    assert user_response.date_updated is not None
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()
