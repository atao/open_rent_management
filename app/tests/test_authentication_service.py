import pytest
from unittest.mock import MagicMock, patch
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from app.services.authentication_service import AuthenticationService
from app.models.user import User
from app.models.auth_errors import AuthError
from app.core.config import Settings


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_oauth2_scheme():
    return MagicMock(spec=OAuth2PasswordBearer)


@pytest.fixture
def auth_service(mock_oauth2_scheme, mock_db):
    return AuthenticationService(oauth2_scheme=mock_oauth2_scheme, db=mock_db)


def test_get_secret_key(auth_service):
    with patch.object(Settings, "secret_key", "test_secret_key"):
        assert auth_service.get_secret_key() == "test_secret_key"

    with patch.object(Settings, "secret_key", None):
        with pytest.raises(ValueError):
            auth_service.get_secret_key()


def test_get_username_from_payload(auth_service):
    token = jwt.encode({"sub": "test_user"}, "test_secret_key", algorithm="HS256")
    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        assert auth_service.get_username_from_payload(token) == "test_user"

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        assert auth_service.get_username_from_payload(None) is None


def test_verify_password(auth_service):
    hashed_password = auth_service.get_password_hash("test_password")
    assert auth_service.verify_password("test_password", hashed_password) is True
    assert auth_service.verify_password("wrong_password", hashed_password) is False


def test_authenticate_user(auth_service, mock_db):
    user = User(email="test@example.com", password=auth_service.get_password_hash("test_password"), disabled=False)

    mock_db.query.return_value.filter.return_value.first.return_value = None

    assert auth_service.authenticate_user("wrong@example.com", "test_password") is False

    mock_db.query.return_value.filter.return_value.first.return_value = user

    assert auth_service.authenticate_user("test@example.com", "test_password") == user

    assert auth_service.authenticate_user("test@example.com", "wrong_password") is False

    user.disabled = True
    with pytest.raises(Exception) as excinfo:
        auth_service.authenticate_user("test@example.com", "test_password")
    assert str(excinfo.value) == AuthError.USER_DISABLED


def test_is_password_secure():
    assert AuthenticationService.is_password_secure("Password1!") is True
    assert AuthenticationService.is_password_secure("password") is False
    assert AuthenticationService.is_password_secure("PASSWORD") is False
    assert AuthenticationService.is_password_secure("Pass1") is False
    assert AuthenticationService.is_password_secure("Password!") is False


def test_login(auth_service):
    with patch.object(auth_service, "create_access_token", return_value="test_access_token"):
        refresh_token = auth_service.login("test@example.com")
        assert refresh_token.access_token == "test_access_token"
        assert refresh_token.token_type == "bearer"
        assert refresh_token.refresh_token == "test_access_token"


def test_create_access_token(auth_service):
    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        token = auth_service.create_access_token(data={"sub": "test_user"})
        payload = jwt.decode(token, "test_secret_key", algorithms=[Settings.algorithm])
        assert payload["sub"] == "test_user"


def test_refresh_access_token(auth_service, mock_db):
    user = User(email="test@example.com", password="test_password", disabled=False)
    mock_db.query.return_value.filter.return_value.first.return_value = user
    refresh_token = jwt.encode({"sub": "test@example.com"}, "test_secret_key", algorithm="HS256")

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        new_token = auth_service.refresh_access_token(refresh_token)
        assert new_token.refresh_token == refresh_token
        assert new_token.token_type == "bearer"

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        with patch.object(auth_service, "get_username_from_payload", return_value=None):
            with pytest.raises(Exception) as excinfo:
                auth_service.refresh_access_token(refresh_token)
            assert str(excinfo.value) == AuthError.INVALID_REFRESH_TOKEN


def test_get_current_active_user(auth_service, mock_db):
    user = User(email="test@example.com", password="test_password", disabled=False)
    mock_db.query.return_value.filter.return_value.first.return_value = user
    token = jwt.encode({"sub": "test@example.com"}, "test_secret_key", algorithm="HS256")

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        active_user = auth_service.get_current_active_user(token)
        assert active_user == user

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        with patch.object(auth_service, "get_username_from_payload", return_value=None):
            with pytest.raises(Exception) as excinfo:
                auth_service.get_current_active_user(token)
            assert str(excinfo.value) == AuthError.COULD_NOT_VALIDATE_CREDENTIALS

    user.disabled = True
    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        with pytest.raises(Exception) as excinfo:
            auth_service.get_current_active_user(token)
        assert str(excinfo.value) == AuthError.USER_DISABLED
