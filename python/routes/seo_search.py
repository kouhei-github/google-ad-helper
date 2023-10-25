from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Dict
from config.index import get_db
from sqlalchemy.orm import Session
from services.google.advertisement.search_word import GoogleAdvertisementSearchWordFacade
from schemas.index import SearchVolumeSchema, SearchWordRequestSchema


seo_route = APIRouter(
    prefix="/api/seo",
    tags=["SEO Search"]
)

@seo_route.post("/", response_model=List[SearchVolumeSchema])
async def search_volume(
    body: SearchWordRequestSchema,
    # db: Session = Depends(get_db),
    # get_bearer_token: TokenDataSchema = Depends(get_current_bearer_token)
):
    """
    Args：
        body (SearchWordRequestSchema)： 検索語を含むリクエストボディ。

    戻り値
        List[SearchVolumeSchema]： 検索ボリュームレスポンスのリスト。
    """
    googleAdsFacade = GoogleAdvertisementSearchWordFacade("9082161719",[2392],1005)
    keyword_ideas = googleAdsFacade.get_keyword_volume_request([body.search_word])

    result: List[SearchVolumeSchema] = []
    for idea in keyword_ideas:
        competition_value = googleAdsFacade.keyword_competition_level_enum.Name(
            idea.keyword_idea_metrics.competition
        )
        search = SearchVolumeSchema(
            word=idea.text, # 検索ワード
            monthly_average=str(idea.keyword_idea_metrics.avg_monthly_searches), # 1ヶ月の平均検索回数
            competition_num=idea.keyword_idea_metrics.competition,
            competition_value=competition_value  # 競合の割合
        )
        result.append(search)

    return result
