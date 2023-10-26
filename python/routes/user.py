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
# 全てのユーザー情報を返すエンドポイントを設定します。
# レスポンスモデルは UserShowSchema のリストとして定義されています。
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

    # ベアラートークンに基づいてユーザー情報をデータベースから取得する。
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()

    # ログインユーザーが存在しない、つまりトークンが無効な場合、エラーレスポンスを返す。
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='is not correct token'
        )

    # データベースから全てのユーザーを取得する。
    query_users = db.query(User).all()

    # データベースから取得したユーザー情報を UserShowSchema の形に整形する。
    users = [ UserShowSchema(id=user.id, name=user.name, email=user.email) for user in query_users ]

    # 整形したユーザーデータのリストを返す。
    return users


@user.get("/{user_id}", response_model= UserShowSchema)
# ユーザのIDをパスパラメータとして受け取り、対応するユーザ情報を返すエンドポイントを設定します。
# レスポンスモデルは UserShowSchema として定義されています。
async def find_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    引数
        user_id (int)： 検索するユーザーのID。
        db (Session)： 使用するデータベース・セッション。

    戻り値
        UserShowSchema： ユーザーの詳細。

    発生
        HTTPException： 指定した ID のユーザが存在しない場合。
    """
    # 指定されたIDでユーザーを検索します。
    login_user = db.query(User).filter(User.id == user_id).first()

    # 該当するユーザーがデータベースに存在しない場合、HTTP 404エラーを返します。
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dose not exist'
        )

    # 該当するユーザが見つかった場合、これを UserShowSchema へマッピングして返す。
    return UserShowSchema(id=login_user.id, name=login_user.name, email=login_user.email)
