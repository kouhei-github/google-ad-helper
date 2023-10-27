from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Dict
from config.index import get_db
from sqlalchemy.orm import Session
from services.google.advertisement.search_word import GoogleAdvertisementSearchWordFacade
from schemas.index import SearchVolumeSchema, SearchWordRequestSchema
from services.openai.gpt.model import GPTModelFacade


seo_route = APIRouter(
    prefix="/api/seo",
    tags=["SEO Search"]
)

# エンドポイント'/' (ルート)に対するPOSTリクエストを設定します。レスポンスモデルはSearchVolumeSchemaのリストです。
@seo_route.post("/", response_model=List[SearchVolumeSchema])
async def search_volume(
        body: SearchWordRequestSchema,
        # db: Session = Depends(get_db),
        # get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token),
        # これらの行は現在コメントアウトされていますが、データベースセッションとベアラートークンの取得を行うために使用できます。
):
    """
    Args：
        body (SearchWordRequestSchema)： 検索語を含むリクエストボディ。

    戻り値
        List[SearchVolumeSchema]： 検索ボリュームレスポンスのリスト。
    """
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



@seo_route.get("/create_letter", response_model=Dict[str,str])
async def search_volume(
        word: str=None,
        # db: Session = Depends(get_db),
        # get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token),
        # 上記の2行は現在コメントアウトされていますが、必要に応じてデータベースセッションとベアラートークンの取得を行うために使用できます。
):
    """
    Args：
        word (str)：文章を作成したいキーワード

    戻り値
        Dict[str,str]： 実行結果。
    """
    # GPTModelFacadeクラスのインスタンスを作成します。
    model = GPTModelFacade()

    # 指定されたwordに基づいて対話タスクを行い、その結果を取得します。
    result = model.listen_prompt(word)

    # 対話の結果を含むディクショナリを返します。
    return {"query": result}

