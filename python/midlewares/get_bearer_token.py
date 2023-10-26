from fastapi import HTTPException, Depends, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from typing import Annotated
from services.jwt_token import verify_token
from schemas.index import TokenDataSchema

# OAuth2PasswordBearerはクライアントがリソース所有者のデータにアクセスするためのトークンを持つ機能を提供します。
# ここでは、"login"というURLでトークンを取得する設定をしています。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# get_current_bearer_tokenはAPIルートで使われ、現在のBearerトークンを取得する関数です。
async def get_current_bearer_token( token: Annotated[str, Depends(oauth2_scheme)]) -> TokenDataSchema:
    """
    引数
        token (Annotated[str, Depends])： クライアントが提供するベアラートークン。

    戻り値
        TokenDataSchema： トークンが有効な場合に検証されたトークン・データ。

    発生
        HTTPException： トークンが無効あるいは検証できない場合は、ステータスコード 401 UNAUTHORIZED の HTTPException が発生します。

    """

    # 認証スキームを設定します。Bearer認証が使用されます。
    authenticate_value = "Bearer"

    # 認証エラーが発生した際に送信するHTTPExceptionを作成します。
    # これは、認証情報が無効または確認できない場合にクライアントに送信されます。
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    # トークンを検証し、その結果（トークンデータ）を返します。トークンが無効な場合は先程定義したHTTPExceptionを送信します。
    return verify_token(token, credentials_exception)
