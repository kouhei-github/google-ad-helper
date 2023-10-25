from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from config.index import get_db
from sqlalchemy.orm import Session
from schemas.index import TokenDataSchema, UserShowSchema
from midlewares.index import get_current_bearer_token
from models.user import User


user = APIRouter(
    prefix="/api/user",
    tags=["User"]
)

@user.get("/", response_model= List[UserShowSchema])
async def read_all_users(
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    引数
        db (Session)： データクエリに使用されるデータベースセッション。
        get_bearer_token (TokenDataSchema)： 認証に使用するベアラートークン。

    戻り値：
        List[UserShowSchema]： 指定されたフィールドを持つユーザーオブジェクトのリスト。

    発生
        HTTPException： ベアラートークンが無効な場合、あるいはトークンがどのユーザーにも属さない場合。
    """
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()

    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='is not correct token'
        )
    query_users = db.query(User).all()

    users = [ UserShowSchema(id=user.id, name=user.name, email=user.email) for user in query_users ]
    return users

@user.get("/{user_id}", response_model= UserShowSchema)
async def find_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    引数
        user_id (int)： 検索するユーザーのID。
        db (Session)： 使用するデータベース・セッション。

    戻り値
        UserShowSchema： ユーザーの詳細。

    発生
        HTTPException： 指定した ID のユーザが存在しない場合。
    """
    login_user = db.query(User).filter(User.id == user_id).first()

    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dose not exist'
        )

    return UserShowSchema(id=login_user.id, name=login_user.name, email=login_user.email)
