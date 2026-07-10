from fastapi import APIRouter, Depends
from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.word import Word
from app.models.word_usage_summary import WordUsageSummary
from app.schemas.statistics import WordStatisticsResponse


router = APIRouter(
    prefix="/api/statistics",
    tags=["statistics"],
)

ADVANCED_CEFR_LEVELS = ("B2", "C1", "C2")


@router.get(
    "",
    response_model=WordStatisticsResponse,
)
def get_word_statistics(
    db: Session = Depends(get_db),
) -> WordStatisticsResponse:
    total_words = (
        db.scalar(
            select(func.count(Word.id))
        )
        or 0
    )

    words_above_b1 = (
        db.scalar(
            select(func.count(Word.id))
            .where(
                Word.cefr_level.in_(ADVANCED_CEFR_LEVELS),
            )
        )
        or 0
    )

    has_usage_summary = exists(
        select(WordUsageSummary.id).where(
            WordUsageSummary.word_id == Word.id,
        )
    )

    enhanced_words = (
        db.scalar(
            select(func.count(Word.id))
            .where(
                Word.cefr_level.in_(ADVANCED_CEFR_LEVELS),
                has_usage_summary,
            )
        )
        or 0
    )

    enhancement_percentage = (
        round((enhanced_words / words_above_b1) * 100, 2)
        if words_above_b1 > 0
        else 0.0
    )

    return WordStatisticsResponse(
        total_words=total_words,
        words_above_b1=words_above_b1,
        enhanced_words=enhanced_words,
        enhancement_percentage=enhancement_percentage,
    )