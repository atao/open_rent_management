import jwt
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session
from app.services.authentication_service import AuthenticationService
from app.models.user import User
from app.core.config import Settings


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_oauth2_scheme():
    return MagicMock()


@pytest.fixture
def auth_service(mock_oauth2_scheme, mock_db):
    return AuthenticationService(oauth2_scheme=mock_oauth2_scheme, db=mock_db)


def test_get_secret_key(auth_service):
    with patch.object(Settings, "secret_key", "test_secret_key"):
        assert auth_service.get_secret_key() == "test_secret_key"

    with patch.object(Settings, "secret_key", None):
        with pytest.raises(ValueError):
            auth_service.get_secret_key()


def test_get_payload(auth_service):
    token = jwt.encode({"sub": "test"}, "test_secret_key", algorithm="HS256")
    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        payload = auth_service.get_payload(token)
        assert payload["sub"] == "test"


def test_verify_password(auth_service):
    hashed_password = auth_service.get_password_hash("test_password")
    assert auth_service.verify_password("test_password", hashed_password)


def test_authenticate_user(auth_service, mock_db):
    user = User(email="test@example.com", password=auth_service.get_password_hash("test_password"))
    mock_db.query().filter().first.return_value = user

    assert auth_service.authenticate_user("test@example.com", "test_password") == user
    assert not auth_service.authenticate_user("test@example.com", "wrong_password")
    mock_db.query().filter().first.return_value = None
    assert not auth_service.authenticate_user("wrong@example.com", "test_password")


def test_is_password_secure(auth_service):
    assert auth_service.is_password_secure("Test@1234")
    assert not auth_service.is_password_secure("test")
    assert not auth_service.is_password_secure("Test1234")
    assert not auth_service.is_password_secure("test@1234")
    assert not auth_service.is_password_secure("TEST@1234")


def test_login(auth_service):
    with patch.object(auth_service, "create_access_token", return_value="test_token"):
        refresh_token = auth_service.login("test@example.com")
        assert refresh_token.access_token == "test_token"
        assert refresh_token.refresh_token == "test_token"


def test_create_access_token(auth_service):
    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        token = auth_service.create_access_token(data={"sub": "test"})
        payload = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
        assert payload["sub"] == "test"


def test_refresh_access_token(auth_service, mock_db):
    user = User(email="test@example.com")
    mock_db.query().filter().first.return_value = user
    refresh_token = jwt.encode({"sub": "test@example.com"}, "test_secret_key", algorithm="HS256")

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        new_token = auth_service.refresh_access_token(refresh_token)
        assert new_token.access_token is not None

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        with patch.object(auth_service, "get_payload", side_effect=ExpiredSignatureError):
            with pytest.raises(HTTPException) as excinfo:
                auth_service.refresh_access_token(refresh_token)
            assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        with patch.object(auth_service, "get_payload", side_effect=InvalidTokenError):
            with pytest.raises(HTTPException) as excinfo:
                auth_service.refresh_access_token(refresh_token)
            assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user(auth_service, mock_db):
    token = jwt.encode({"sub": "test@example.com"}, "test_secret_key", algorithm="HS256")
    user = User(email="test@example.com")
    mock_db.query().filter().first.return_value = user

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        current_user = await auth_service.get_current_user(token)
        assert current_user == user

    with patch.object(auth_service, "get_secret_key", return_value="test_secret_key"):
        with patch.object(auth_service, "get_payload", side_effect=InvalidTokenError):
            with pytest.raises(HTTPException) as excinfo:
                await auth_service.get_current_user(token)
            assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_active_user(auth_service, mock_db):
    user = User(email="test@example.com", disabled=False)
    mock_db.query().filter().first.return_value = user

    current_user = await auth_service.get_current_active_user(user)
    assert current_user == user

    user.disabled = True
    with pytest.raises(HTTPException) as excinfo:
        await auth_service.get_current_active_user(user)
    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
