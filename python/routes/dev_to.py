# fastapiとその他必要なライブラリをインポートします。
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from config.index import get_db
from sqlalchemy.orm import Session
from schemas.index import TokenDataSchema
from midlewares.index import get_current_bearer_token
from models.user import User
from services.crawling.dev_to.get_articles import GetArticlesInDevTo
from services.markdown.changer import ConvertUrlToMarkdown
from services.google.spread_sheet.spread_sheet_facade import SpreadSheetFacade

# /api/dev-to というプレフィックスと"Dev-To-Crawling"というタグのついたAPIRouterを作成します。
dev_to_router = APIRouter(
    prefix="/api/dev-to",
    tags=["Dev-To-Crawling"]
)

# /latestエンドポイントを作成します。このエンドポイントは、dev.toから最新の記事を取得しスプレッドシートに保存します。
@dev_to_router.get("/latest", response_model=List[str])
async def get_dev_to_latest_articles(
        page: int = 10,
        db: Session = Depends(get_db),
        get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    引数
        page (int)： 検索する最新記事の数。デフォルトは10。
        db (セッション)： データベースとやりとりするためのセッションオブジェクト。
        get_bearer_token（TokenDataSchema）： ベアラートークンのデータスキーマ。

    戻り値
        リスト[str]： 成功メッセージを含むリスト。

    """

    # get_bearer_token.idを用いてユーザーを検索します。
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()

    # ユーザーが存在しない場合、HTTPエラー404を返します。
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dose not exist'
        )

    # dev.toから最新記事を取得するインスタンスを作成します。
    dev_to_get_article_facade = GetArticlesInDevTo("https://dev.to/api/articles/latest")
    dev_to_get_article_facade.get_article()

    # 記事のURLを取得します。

    # スプレッドシートへの書き込みを行うインスタンスを作成します。
    spread_facade = SpreadSheetFacade("1mjk98TSpRJ2ixsYfJ5rp4Zw0Pr8EeDV_YNS5VdO4jnM", "write")
    _ = spread_facade.get_values("SEO")

    result = []
    for article in dev_to_get_article_facade.json:
        positive_reactions_count = article.get("positive_reactions_count", 0)
        if positive_reactions_count < 5:
            continue

        # URLに基づいてMarkdown形式のテキストを取得します。
        link = article.get("url", 0)
        convert_markdown = ConvertUrlToMarkdown.convert(link)
        result.append([link, convert_markdown])

    # スプレッドシートに書き込みます。
    await spread_facade.write_sheet("SEO", result)

    # 成功メッセージを返します。
    return [f'成功しました: 計{len(result)}件保存']

# /popular エンドポイントを作成します。使用は未定義で、まだ何も行いません。
@dev_to_router.get("/popular", response_model=List[str])
async def get_dev_to_popular_articles(
        rank: int,
        db: Session = Depends(get_db),
        get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    引数
        page (int)： 検索する最新記事の数。デフォルトは10。
        db (セッション)： データベースとやりとりするためのセッションオブジェクト。
        get_bearer_token（TokenDataSchema）： ベアラートークンのデータスキーマ。

    戻り値
        リスト[str]： 成功メッセージを含むリスト。

    """

    # get_bearer_token.idを用いてユーザーを検索します。
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()

    # ユーザーが存在しない場合、HTTPエラー404を返します。
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dose not exist'
        )
    # このパラメータを使用すると、クライアントは過去数日間で最も人気のある記事を返すことができますN。
    # top返された記事の公開からの日数を示します。
    # このパラメータは と組み合わせて使用できますtag。
    dev_to_get_article_facade = GetArticlesInDevTo(
        f'https://dev.to/api/articles?top={rank}')
    dev_to_get_article_facade.get_article()

    # スプレッドシートへの書き込みを行うインスタンスを作成します。
    spread_facade = SpreadSheetFacade("1mjk98TSpRJ2ixsYfJ5rp4Zw0Pr8EeDV_YNS5VdO4jnM", "write")
    _ = spread_facade.get_values("SEO")

    result = []
    for article in dev_to_get_article_facade.json:
        positive_reactions_count = article.get("positive_reactions_count", 0)
        if positive_reactions_count < 5:
            continue

        # URLに基づいてMarkdown形式のテキストを取得します。
        link = article.get("url", 0)
        convert_markdown = ConvertUrlToMarkdown.convert(link)
        result.append([link, convert_markdown])

    # スプレッドシートに書き込みます。
    await spread_facade.write_sheet("SEO", result)

    # 成功メッセージを返します。
    return [f'成功しました: 計{len(result)}件保存']
@dev_to_router.get("/tag/{tag}", response_model=List[str])
async def get_dev_to_popular_articles(
        tag: str,
        db: Session = Depends(get_db),
        get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    引数
        page (int)： 検索する最新記事の数。デフォルトは10。
        db (セッション)： データベースとやりとりするためのセッションオブジェクト。
        get_bearer_token（TokenDataSchema）： ベアラートークンのデータスキーマ。

    戻り値
        リスト[str]： 成功メッセージを含むリスト。

    """

    # get_bearer_token.idを用いてユーザーを検索します。
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()

    # ユーザーが存在しない場合、HTTPエラー404を返します。
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dose not exist'
        )

    # dev.toからタグで検索して記事を取得するインスタンスを作成します。
    dev_to_get_article_facade = GetArticlesInDevTo(
        f'https://dev.to/api/articles?tag={tag}')
    dev_to_get_article_facade.get_article()

    # スプレッドシートへの書き込みを行うインスタンスを作成します。
    spread_facade = SpreadSheetFacade("1mjk98TSpRJ2ixsYfJ5rp4Zw0Pr8EeDV_YNS5VdO4jnM", "write")
    _ = spread_facade.get_values("SEO")

    result = []
    for article in dev_to_get_article_facade.json:
        positive_reactions_count = article.get("positive_reactions_count", 0)
        if positive_reactions_count < 5:
            continue

        # URLに基づいてMarkdown形式のテキストを取得します。
        link = article.get("url", 0)
        convert_markdown = ConvertUrlToMarkdown.convert(link)
        result.append([link, convert_markdown])

    # スプレッドシートに書き込みます。
    await spread_facade.write_sheet("SEO", result)

    # 成功メッセージを返します。
    return [f'成功しました: 計{len(result)}件保存']
