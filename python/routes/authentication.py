from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI関連のモジュールをインポートします。
from sqlalchemy.orm import Session  # SQLAlchemyのセッションをインポートします。

# 以下のモジュールをインポートします：
from config.index import get_db  # データベースセッションを取得する関数。
from models.index import User  # Userモデル。
from services.hashing import Hash  # パスワードハッシュ化クラス。
from services.jwt_token import create_access_token, create_refresh_token  # JWT暗号トークンを生成。
from schemas.index import SignUpSchema, LoginSchema, UserOutSchema  # 入力と出力のスキーマ。

auth = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

@auth.post('/signup', summary="Create new user", response_model=UserOutSchema)  # POSTリクエストのエンドポイントを定義します。
async def create_user(data: SignUpSchema, db: Session = Depends(get_db)):  # 非同期関数で、新規ユーザー作成を処理します。
    """
    Args：
        data (SignUpSchema)： ユーザーのサインアップ情報を含むデータ。
        db (セッション)： データベース・セッション。
    戻り値
        dict： ユーザの名前、メールアドレス、アクセストークン、リフレッシュトークン、トークンタイプを含む辞書。
    発生
        HTTPException： 同じメールアドレスを持つユーザが既にデータベースに存在する場合。
    """
    # データベースから既存のユーザーをクエリーし、存在確認をします。
    user = db.query(User).filter(User.email == data.email).first()
    if user is not None:
        # 同じメールアドレスを持つユーザーが存在する場合は、HTTP例外を発生させます。
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    # ハッシュ処理のインスタンスを生成します。
    hash_facade = Hash()

    # 新しいユーザーオブジェクトを作成します。
    user = User()
    user.name = data.name  # 名前を設定します。
    user.email = data.email  # メールアドレスを設定します。
    user.password = hash_facade.bcript(data.password)  # ハッシュ化したパスワードを設定します。

    # ユーザーオブジェクトをデータベースに追加し、コミット（保存）します。
    db.add(user)
    db.commit()

    # 新規ユーザーの情報を含む辞書を返します。
    return {
        "name": user.name,
        "email": user.email,
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

# ログインAPIのEndpoint
# 成功した場合のHTTPステータスコードは201。レスポンスモデルはUserOutSchema。
@auth.post("/login", summary="Login" ,status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
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
    # ユーザーのメールを使ってデータベースから情報を取得します。
    user = db.query(User).filter(User.email == request.email).first()

    # もしメールがデータベースに存在しない場合、HTTPExceptionをスローします。
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect email or password'
        )
    # データベース保存のhash化されたパスワードを取得します。
    hash_facade = Hash()
    hashed_pass = user.password

    # もしパスワードがマッチしなければ、HTTPExceptionをスローします。
    if not hash_facade.verify(hashed_pass, request.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email or password"
        )

    # 最後にユーザー名、メール、アクセストークン、レフレッシュトークン、トークンタイプをレスポンスとして返します。
    return  {
        "name": user.name,
        "email": user.email,
        # 各ユーザーにユニークなアクセストークンを生成します。
        "access_token": create_access_token(user.id),
        # レフレッシュトークンも同様に生成します。
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }
