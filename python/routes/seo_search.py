from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter, Depends, status, HTTPException, responses
from typing import List, Dict
from config.index import get_db
from sqlalchemy.orm import Session
from services.google.advertisement.search_word import GoogleAdvertisementSearchWordFacade
from schemas.index import SearchVolumeSchema, SearchWordRequestSchema
from services.openai.gpt.model import GPTModelFacade
from services.google.spread_sheet.spread_sheet_facade import SpreadSheetFacade
from schemas.index import TokenDataSchema, ShowArticleResponseSchema
from midlewares.index import get_current_bearer_token
from models.index import User


seo_route = APIRouter(
    prefix="/api/seo",
    tags=["SEO Search"]
)

# エンドポイント'/' (ルート)に対するPOSTリクエストを設定します。レスポンスモデルはSearchVolumeSchemaのリストです。
@seo_route.post("/", response_model=List[SearchVolumeSchema])
async def search_volume(
        body: SearchWordRequestSchema,
        db: Session = Depends(get_db),
        get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token),
        # これらの行は現在コメントアウトされていますが、データベースセッションとベアラートークンの取得を行うために使用できます。
):
    """
    Args：
        body (SearchWordRequestSchema)： 検索語を含むリクエストボディ。

    戻り値
        List[SearchVolumeSchema]： 検索ボリュームレスポンスのリスト。
    """

    # ログインユーザーが存在しない、つまりトークンが無効な場合、エラーレスポンスを返す。
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='is not correct token'
        )

    # GoogleAdvertisementSearchWordFacadeを初期化します。この初期化はGoogle Ads APIとのコミュニケーション準備を行います。
    googleAdsFacade = GoogleAdvertisementSearchWordFacade("9082161719",[2392],1005)

    # Google Ads APIに対してキーワードの検索ボリュームを要求します。
    keyword_ideas = googleAdsFacade.get_keyword_volume_request([body.search_word])

    result: List[SearchVolumeSchema] = []
    for idea in keyword_ideas:
        # Google Ads APIから取得した各キーワードの検索ボリュームを解析します。

        # 競合の割合を取得します。
        competition_value = googleAdsFacade.keyword_competition_level_enum.Name(
            idea.keyword_idea_metrics.competition
        )

        # SearchVolumeSchemaを作成します。
        search = SearchVolumeSchema(
            word=idea.text,  # 検索ワード
            monthly_average=str(idea.keyword_idea_metrics.avg_monthly_searches),  # 1ヶ月の平均検索回数
            competition_num=idea.keyword_idea_metrics.competition,
            competition_value=competition_value  # 競合の割合
        )

        # SearchVolumeSchemaをリターン用のリストに追加します。
        result.append(search)

    # 検索ボリュームデータのリストをリターンします。
    return result



@seo_route.get("/create_letter", response_model=Dict[str,str])  # create_letterエンドポイントにGETリクエストをルーティングします。レスポンスモデルとして辞書形式（キーと値が両方とも文字列）を指定しています。
async def search_volume(
        word: str=None,  # word引数は、作成する文章のキーワードを指定するためのものです。デフォルトではNoneを指定します。
        db: Session = Depends(get_db),  # この行は現在コメントアウトされていますが、データベースセッションを取得するための依存関係を指定するためのものです。この依存関係は、データベースとのインタラクションが必要な場合にコメントアウトを外して使用します。
        get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token),  # この行は現在コメントアウトされていますが、ベアラートークンを取得するための依存関係を指定するためのものです。この依存関係は、認証が必要な場合にコメントアウトを外して使用します。
):
    """
    Args：
        word (str)：文章を作成したいキーワード

    戻り値
        Dict[str,str]： 実行結果。
    """

    # ログインユーザーが存在しない、つまりトークンが無効な場合、エラーレスポンスを返す。
    login_user = db.query(User).filter(User.id == get_bearer_token.id).first()
    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='is not correct token'
        )

    # GPTModelFacadeクラスのインスタンスを作成します。このクラスは、GPTモデルとのインタラクションを簡単に行うためのクラスです。
    model = GPTModelFacade()

    # listen_promptメソッドは、与えられたキーワードに基づいてGPTモデルから文章を生成し、その結果を返します。
    result = await model.listen_prompt(word)

    # SpreadSheetFacadeクラスのインスタンスを作成します。このクラスは、Googleスプレッドシートとのインタラクションを簡単に行うためのクラスです。
    spread_facade = SpreadSheetFacade("1mjk98TSpRJ2ixsYfJ5rp4Zw0Pr8EeDV_YNS5VdO4jnM", "write")

    # get_valuesメソッドで"SEO"シートの値を取得します。ただし、この値は実際には使用されていません（結果を"_"に代入することで明示的に無視しています）。
    _ = spread_facade.get_values("SEO")

    # write_sheetメソッドで"SEO"シートにキーワードと結果のリストを書き込みます。
    await spread_facade.write_sheet("SEO", [[word, result]])

    # "query": "Create"というキーと値のペアを含むディクショナリを返します。これがこの関数の返り値です。
    return {"query": "Create"}

@seo_route.get(
    "/show/{article_id}",
    response_model=ShowArticleResponseSchema,
    summary="記事情報をスプレッドシートから取得する"
)
async def get_article_making_gpt(article_id: int):
    print(article_id)
    spread_sheet_facade = SpreadSheetFacade(
        "1mjk98TSpRJ2ixsYfJ5rp4Zw0Pr8EeDV_YNS5VdO4jnM",
        "read"
    )

    articles = spread_sheet_facade.get_values("SEO")
    if len(articles) < article_id or article_id == 0:
        return responses.JSONResponse(content="Not Found", status_code=404)

    return ShowArticleResponseSchema(description=articles[article_id][1])
