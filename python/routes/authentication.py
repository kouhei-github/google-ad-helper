from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.index import get_db
from models.index import User
from services.hashing import Hash
from services.jwt_token import create_access_token, create_refresh_token
from schemas.index import SignUpSchema, LoginSchema, UserOutSchema

auth = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

@auth.post('/signup', summary="Create new user", response_model=UserOutSchema)
async def create_user(data: SignUpSchema, db: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    hash_facade = Hash()
    user = User()
    user.name = data.name
    user.email = data.email
    user.password = hash_facade.bcript(data.password)
    db.add(user)
    db.commit()
    return {
        "name": user.name,
        "email": user.email,
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

@auth.post("/login", status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
async def login(request: LoginSchema, db: Session = Depends(get_db)):
    """
    引数:
        request (LoginSchema): ログインリクエストを表すデータ。
        db (Session): データベースセッション。

    戻り値:
        dict: 生成されたアクセストークンとトークンタイプ。

    例外:
        HTTPException: ユーザーが見つからないか、パスワードが間違っている場合。
    """
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password'
        )

    hash_facade = Hash()
    hashed_pass = user.password
    if not hash_facade.verify(hashed_pass, request.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email or password"
        )

    return  {
        "name": user.name,
        "email": user.email,
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

