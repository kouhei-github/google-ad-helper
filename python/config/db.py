from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 環境変数を読み込みます。これらはデータベースとの接続に使用されます。
port = os.environ["PORT"]
user = os.environ["USERNAME"]
password = os.environ["USERPASS"]
database = os.environ["DATABASE"]
host = os.environ["HOST"]

# SQLAlchemy の create_engine を使ってデータベースエンジン（接続）を作成します。
# 接続の文字列は環境変数に基づいてフォーマットされます。
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')

# SQLAlchemy のセッションメーカーを作成します。エンジンをこれにバインドして使用します。
# これにより、デーアベースセッションが作成されます。
SessionLocal = sessionmaker(bind=engine)

# データベースモデルを作成するために使用する基底クラスを作成します。
# これは、SQLAlchemy の機能を使ってデータベースを連携させる仕組みの一部となります。
Base = declarative_base()

# get_db 関数はデータベースセッションを生成し、そのコンテキストが終了するとセッションをクローズします。
# このコードはSQLAlchemyのセッションライフサイクルとよく組み合わせて使われます。
def get_db():
    # セッションを生成します。
    db = SessionLocal()
    try:
        # セッションを利用できるようにする（yieldする）。
        yield db
    finally:
        # 最後にセッションをクローズします。
        db.close()
