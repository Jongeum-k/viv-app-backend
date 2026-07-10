from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field


class WordListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lemma: str
    part_of_speech: str | None = None
    cefr_level: str | None = None
    frequency_rank: int | None = None
    frequency_score: float | None = None
    difficulty_score: float | None = None
    source_count: int


class PaginatedWordsResponse(BaseModel):
    items: list[WordListItem]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)
    has_next: bool
    has_previous: bool


class WordDefinitionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider_name: str
    language_code: str
    phonetic: str | None = None
    definition_summary: str | None = None


class WordSearchResultItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider_name: str
    query_text: str
    result_rank: int
    title: str | None = None
    snippet: str | None = None
    url: str | None = None
    domain: str | None = None


class WordTopicScoreItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_name: str
    provider_name: str
    score: float
    evidence_count: int


class WordUsageSummaryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider_name: str
    model_name: str
    prompt_version: str
    summary: str


class WordDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lemma: str
    part_of_speech: str | None = None
    cefr_level: str | None = None
    frequency_rank: int | None = None
    frequency_score: float | None = None
    difficulty_score: float | None = None
    source_count: int

    definitions: list[WordDefinitionItem]
    search_results: list[WordSearchResultItem]
    topic_scores: list[WordTopicScoreItem]
    usage_summaries: list[WordUsageSummaryItem]


PageParam = Annotated[int, Query(ge=1)]
PageSizeParam = Annotated[int, Query(ge=1, le=100)]