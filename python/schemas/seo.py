from pydantic import BaseModel

class SearchVolume(BaseModel):
    word: str
    monthly_average: str
    competition_num: int
    competition_value: str

class SearchWordRequest(BaseModel):
    search_word: str

class ShowArticleResponse(BaseModel):
    description: str
