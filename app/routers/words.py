from math import ceil

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models.word import Word
from app.models.word_usage_summary import WordUsageSummary
from app.schemas.word import (
    PageParam,
    PageSizeParam,
    PaginatedWordsResponse,
    WordDetailResponse,
)

router = APIRouter(
    prefix="/api/words",
    tags=["words"],
)

ADVANCED_CEFR_LEVELS = ("B2", "C1", "C2")


@router.get(
    "",
    response_model=PaginatedWordsResponse,
)
def get_words(
    page: PageParam = 1,
    page_size: PageSizeParam = 20,
    db: Session = Depends(get_db),
) -> PaginatedWordsResponse:
    offset = (page - 1) * page_size

    has_usage_summary = exists(
        select(WordUsageSummary.id).where(
            WordUsageSummary.word_id == Word.id,
        )
    )

    filters = (
        Word.cefr_level.in_(ADVANCED_CEFR_LEVELS),
        has_usage_summary,
    )

    total_items = (
        db.scalar(
            select(func.count(Word.id))
            .select_from(Word)
            .where(*filters)
        )
        or 0
    )

    statement = (
        select(Word)
        .where(*filters)
        .order_by(
            Word.frequency_rank.asc().nulls_last(),
            Word.lemma.asc(),
            Word.id.asc(),
        )
        .offset(offset)
        .limit(page_size)
    )

    words = db.scalars(statement).all()

    total_pages = ceil(total_items / page_size) if total_items else 0

    return PaginatedWordsResponse(
        items=list(words),
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1 and total_pages > 0,
    )


@router.get(
    "/{word_id}",
    response_model=WordDetailResponse,
)
def get_word(
    word_id: int,
    db: Session = Depends(get_db),
) -> WordDetailResponse:
    statement = (
        select(Word)
        .where(
            Word.id == word_id,
            Word.cefr_level.in_(ADVANCED_CEFR_LEVELS),
        )
        .options(
            selectinload(Word.definitions),
            selectinload(Word.search_results),
            selectinload(Word.topic_scores),
            selectinload(Word.usage_summaries),
        )
    )

    word = db.scalar(statement)

    if word is None:
        raise HTTPException(
            status_code=404,
            detail="Word not found.",
        )

    word.definitions.sort(
        key=lambda definition: (
            definition.language_code,
            definition.provider_name,
            definition.id,
        )
    )

    word.search_results.sort(
        key=lambda result: (
            result.result_rank,
            result.id,
        )
    )

    word.topic_scores.sort(
        key=lambda topic_score: (
            -float(topic_score.score),
            topic_score.topic_name,
            topic_score.id,
        )
    )

    word.usage_summaries.sort(
        key=lambda usage_summary: (
            usage_summary.provider_name,
            usage_summary.model_name,
            usage_summary.prompt_version,
            usage_summary.id,
        )
    )

    return WordDetailResponse.model_validate(word)