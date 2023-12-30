from schemas.index import  ShowArticleResponseSchema
from models.index import Article, Tag
from fastapi import APIRouter, Depends, status, HTTPException, responses
from config.index import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import asc


article = APIRouter(
    prefix="/api/article",
    tags=["SEO Search"]
)

@article.get(
    "/all",
    response_model=List[ShowArticleResponseSchema],
    summary="記事情報をスプレッドシートから取得する"
)
async def get_article_all(page=1, db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(asc(Article.id)).offset((int(page)-1)*10).limit(9).all()

    articles = [ShowArticleResponseSchema(ogp_image=article.og_image_url, id=article.id, description=article.description,story="",title=article.title,tags=[tag.name for tag in article.tags]) for article in articles]

    return articles


@article.get(
    "/latest",
    response_model=List[ShowArticleResponseSchema],
    summary="記事情報をスプレッドシートから取得する"
)
async def get_article_latest(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.created_at.desc()).limit(10).all()

    articles = [ShowArticleResponseSchema(ogp_image=article.og_image_url, id=article.id, description=article.description,story="",title=article.title,tags=[tag.name for tag in article.tags]) for article in articles]

    return articles


@article.get(
    "/show/{article_id}",
    response_model=ShowArticleResponseSchema,
    summary="記事情報をスプレッドシートから取得する"
)
async def get_article_by_id(article_id: int, db: Session = Depends(get_db),):
    article: Article = db.query(Article).get(article_id)

    if article is None:
        return responses.JSONResponse(content="Not Found", status_code=404)

    return ShowArticleResponseSchema(
        ogp_image=article.og_image_url,
        id=article.id,
        description=article.description,
        story=article.story,
        title=article.title,
        tags=[tag.name for tag in article.tags]
    )
