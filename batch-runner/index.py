from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.index import dev_to_router

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

# FastAPIアプリケーションにルーティングを追加します。
app.include_router(dev_to_router)
