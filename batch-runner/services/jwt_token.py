import os
from fastapi import HTTPException
from datetime import  datetime, timedelta
from jose import JWTError, jwt
from typing import Union, Any
from schemas.index import TokenDataSchema


JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15 # 15 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days


def create_access_token(subject: Union[str, Any], expires_delta: timedelta | None = None):
    """
    引数
        件名： Union[str, Any]. アクセストークンの件名。文字列でも他の型でもよい。
        expires_delta: timedelta | なし。アクセストークンの有効期限。指定した場合、トークンの有効期間を指定します。省略した場合はデフォルトの
    * 有効期限が使用されます。

    戻り値
        str. エンコードされたアクセストークン。

    発生します：
        HTTPException： アクセストークンの作成に失敗した場合。
        JWTError： アクセストークンのエンコードにエラーがあった場合。
    """

    # expires_deltaが指定されている場合、それを使用して有効期限を計算します。
    # 指定されていない場合、デフォルト値を使用します。
    if expires_delta:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # トークンに含める情報を設定します。expires_deltaとsubjectを含めます。
    to_encode = {"exp": expires_delta, "sub": str(subject)}

    # トークンをエンコードします。
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    # エンコードされたトークンを戻り値として返します。
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    この関数は、指定された主題(subject)および期限(expires_delta)をもとにリフレッシュトークンを作成します。

    Arguments:
    subject (Union[str, Any])： リフレッシュトークンの件名。文字列または他の型。
    expires_delta (int, オプション)： リフレッシュトークンの有効期限を秒単位で指定します。指定しない場合は、デフォルトの有効期限が使用されます。デフォルトはNone。

    Returns:
    str： エンコードされたリフレッシュトークン。

    Raises:
    HTTPException： JWT のエンコードに失敗した場合、あるいは有効期限が無効な場合。

    """
    if expires_delta is not None:
        # 有効期限が指定されている場合、その期間を現在の時間に追加します。
        expires_delta = datetime.utcnow() + expires_delta
    else:
        # 有効期限が指定されていない場合、デフォルトの期間(分単位)を現在の時間に追加します。
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    # 有効期限と主題をエンコードします。
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    # エンコードされたJWTを生成します。
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    # エンコードされたJWTをreturnします。
    return encoded_jwt

def verify_token(token: str, credentials_exception: HTTPException) -> TokenDataSchema:
    """
    この関数は、与えられたトークンを検証し、トークンからユーザーIDを取得して返します。

    Arguments:
    token (str)： 検証するトークンの文字列。
    credentials_exception (HTTPException)： トークンが無効である場合に発生する例外。

    Returns:
    TokenDataSchema： デコードされたトークンデータをTokenDataSchemaインスタンスとして返します。

    """
    try:
        # トークンをデコードします。トークンをデコードする際は、秘密鍵とアルゴリズムに基づいています。
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        # デコードされたペイロードからuser_idを取得します。
        user_id: str = payload.get("sub")

        # user_idがNoneの場合、例外を発生させます。
        if user_id is None:
            raise credentials_exception
        # インスタンスTokenDataSchemaを作成し、user_idを整数として返します。
        return TokenDataSchema(user_id=int(user_id))
    except JWTError:
        # JWTのデコード中にエラーが発生した場合、資格情報の例外を発生させます。
        raise credentials_exception
