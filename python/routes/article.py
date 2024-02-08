from schemas.index import  ShowArticleResponseSchema, TagResponseSchema
from models.index import Article, Tag
from fastapi import APIRouter, Depends, status, HTTPException, responses
from config.index import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import asc


article = APIRouter(
    prefix="/api/article",
    tags=["記事情報取得"]
)

@article.get(
    "/all",
    response_model=List[ShowArticleResponseSchema],
    summary="記事情報を一覧ページを取得"
)
async def get_article_all(page=1, db: Session = Depends(get_db)):
    """
    Args:
        page (int, optional): ページ番号。デフォルトは1。表示する記事情報の一覧ページの番号を指定します。
        db (Session, optional): データベースセッション。デフォルトはget_db関数から取得したセッション。データベースへの接続に使用されます。

    """
    articles = db.query(Article).order_by(asc(Article.id)).offset((int(page)-1)*10).limit(9).all()

    articles = [ShowArticleResponseSchema(ogp_image=article.og_image_url, id=article.id, description=article.description,story="",title=article.title,tags=[tag.name for tag in article.tags]) for article in articles]

    return articles


@article.get(
    "/latest",
    response_model=List[ShowArticleResponseSchema],
    summary="記事情報を最新順で取得する"
)
async def get_article_latest(page=1, db: Session = Depends(get_db)):
    """
    引数
        page (int, optional): ページ番号。デフォルトは1。表示する記事情報の一覧ページの番号を指定します。
        db (セッション)： データベースセッションオブジェクト

    戻り値
        リスト[ShowArticleResponseSchema]： 最新の記事のリスト

    概要
        データベースから最新の記事を取得する。

    説明
        このメソッドは最新の記事を取得するためにデータベースに問い合わせます。作成日の降順で記事を並べ、結果を 10 件に制限します。各記事は
    * オブジェクトは記事の情報を表示するために必要なフィールドを含む ShowArticleResponseSchema オブジェクトに変換されます。このメソッドは次に、これらの変換された
    * のリストを返します。

    例
        articles = get_article_latest(db)
    """
    articles = db.query(Article).order_by(Article.created_at.desc()).offset((int(page)-1)*10).limit(9).all()

    articles = [ShowArticleResponseSchema(ogp_image=article.og_image_url, id=article.id, description=article.description,story="",title=article.title,tags=[tag.name for tag in article.tags]) for article in articles]

    return articles


@article.get(
    "/show/{article_id}",
    response_model=ShowArticleResponseSchema,
    summary="記事の詳細情報を取得する"
)
async def get_article_by_id(article_id: int, db: Session = Depends(get_db),):
    """
    Args:
        article_id (int): 記事のID
        db (Session): データベースセッション

    Returns:
        ShowArticleResponseSchema: 記事の詳細情報

    Summary:
        指定された記事の詳細情報を取得するメソッドです。

    """
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

@article.get("/tag/{slug}", response_model=List[ShowArticleResponseSchema],summary="タグで記事を検索する")
async def get_article_by_slug(slug: str, page=1, db: Session = Depends(get_db)):
    """
    Args:
        slug (str): タグのスラグ
        page (int, optional): ページ番号（デフォルト値: 1）
        db (Session, optional): データベースセッション（デフォルト値: 依存関数 `get_db` により取得）

    Returns:
        List[ShowArticleResponseSchema]: 記事のリスト

    Summary:
        タグで記事を検索するメソッド

    Description:
        指定されたタグの記事をデータベースから検索し、ページネーションを考慮して記事のリストを返します。

        Args:
            - `slug` (str): タグのスラグ
            - `page` (int, optional): ページ番号（デフォルト値: 1）
            - `db` (Session, optional): データベースセッション（デフォルト値: 依存関数 `get_db` により取得）

        Returns:
            - `List[ShowArticleResponseSchema]`: 記事のリスト
                - `ogp_image` (str): 記事のOGP画像URL
                - `id` (int): 記事のID
                - `description` (str): 記事の説明文
                - `story` (str): 記事の本文
                - `title` (str): 記事のタイトル
                - `tags` (List[str]): 記事のタグのリスト

        Raises:
            - `404 Not Found`: 指定されたタグが存在しない場合、エラーレスポンスとして "Not Found" を返します。
    """
    tag = db.query(Tag).filter_by(name=slug).one_or_none()
    if tag is None:
        return responses.JSONResponse(content="Not Found", status_code=404)

    items_per_page = 18  # 1ページあたりの表示件数
    # calculating offset
    offset = (int(page) - 1) * items_per_page
    articl_query = db.query(Article).filter(Article.tags.any(Tag.id == tag.id)).limit(items_per_page).offset(offset)
    articles = [ShowArticleResponseSchema(ogp_image=article.og_image_url, id=article.id, description=article.description,story="",title=article.title,tags=[tag.name for tag in article.tags]) for article in articl_query]
    return articles
