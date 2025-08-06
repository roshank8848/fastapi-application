from pydantic import BaseModel


class TokenData(BaseModel):
    name: str
    preferred_username: str 
    sub: str
    email: str | None = None
    roles: list[str] = []
