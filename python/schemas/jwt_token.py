from pydantic import  BaseModel
from typing import List

class TokenData:
    def __init__(self,  user_id: int=None,  scopes: List[str]=None):
        self.id: int | None = user_id
        self.scopes: list[str] = scopes

class LoginData(BaseModel):
    email: str
    password: str
