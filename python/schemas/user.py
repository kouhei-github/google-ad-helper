from pydantic import  BaseModel

class SignUp(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    name: str
    email: str
    access_token: str
    refresh_token: str
    token_type: str

class UserShow(BaseModel):
    id: int
    name: str
    email: str
