from pydantic import BaseModel

class SearchVolume(BaseModel):
    word: str
    monthly_average: str
    competition: str

