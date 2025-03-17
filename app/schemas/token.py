from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(Token):
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None
