from fastapi import APIRouter, Depends
from typing import List
from config.index import get_db
from sqlalchemy.orm import Session
from schemas.index import TokenDataSchema
from midlewares.index import get_current_bearer_token


health_check = APIRouter(
    prefix="/api/health",
    tags=["Health Check"]
)

@health_check.get("/")
async def health():
    return {"msg": "I am good health."}

@health_check.get("/bearer", response_model= List[str])
async def read_all_users(
    db: Session = Depends(get_db),
    get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """データベースから全てのユーザーを読み込む

    Args:
        db (Session):  使用するデータベースセッション

    Returns:
        List[ShowUserSchema]: 全ユーザのリスト

    Raises:
        HTTPException: データベースからユーザーを取得する際にエラーが発生した場合

    """
    print(get_bearer_token)
    return {}
