from pydantic import BaseModel, Field


class WordStatisticsResponse(BaseModel):
    total_words: int = Field(ge=0)
    words_above_b1: int = Field(ge=0)
    enhanced_words: int = Field(ge=0)
    enhancement_percentage: float = Field(ge=0, le=100)