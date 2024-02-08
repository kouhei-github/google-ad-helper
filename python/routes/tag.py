from schemas.index import  ShowArticleResponseSchema, TagResponseSchema
from models.index import Article, Tag
from fastapi import APIRouter, Depends, status, HTTPException, responses
from config.index import get_db
from sqlalchemy.orm import Session
from typing import List

tag = APIRouter(
    prefix="/api/tag",
    tags=["タグを取得"]
)

@tag.get("/all", response_model=List[TagResponseSchema], summary="タグ名一覧を取得する")
async def get_all_tags(page=1, db: Session =Depends(get_db)):
    """
    Args:
        page (int): ページ番号。デフォルト値は1。
        db (Session): データベースセッション。

    Returns:
        List[TagResponseSchema]: タグ名のリスト。各タグはTagResponseSchemaオブジェクトで、idとnameのプロパティを持つ。

    """
    items_per_page = 200  # 1ページあたりの表示件数
    # calculating offset
    offset = (int(page) - 1) * items_per_page
    tags = db.query(Tag).limit(items_per_page).offset(offset)
    return [TagResponseSchema(id=tag.id, name=tag.name) for tag in tags]
