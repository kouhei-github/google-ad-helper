from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mangum import Mangum
from routes.index import (
    auth,
    health_check,
    user,
    seo_route,
)

from config.index import Base, engine

# FastAPIインスタンスを作成
app = FastAPI()

# CORSミドルウェアを追加します。これにより、すべてのオリジン、メソッド、ヘッダーからのリクエストを許可します。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLAlchemyのモデルを元に、データベーススキーマを作成します。
Base.metadata.create_all(bind=engine)

# Mangumを使用してFastAPIアプリケーションをAWS Lambdaと互換性のある形式に変換します。
handler = Mangum(app)

# FastAPIアプリケーションにルーティングを追加します。
app.include_router(auth)
app.include_router(health_check)
app.include_router(user)
app.include_router(seo_route)
