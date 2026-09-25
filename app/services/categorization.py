from typing import Optional

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Category

settings = get_settings()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"


def categorize(description: str, allowed_categories: list[str]) -> str | None:
    if not allowed_categories:
        return None
    prompt = (
        f"Классифицируй трату по описанию в ОДНУ из категорий: {', '.join(allowed_categories)}. "
        f"Ответь только названием категории, без пояснений, одним словом.\n\n"
        f"Описание: {description}"
    )

    response = httpx.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {settings.groq_api_key}"},
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 100,
        },
    )

    data = response.json()
    category = data["choices"][0]["message"]["content"]

    if category not in allowed_categories:
        return None

    return category

def resolve_category_id(
    category_id: Optional[int],
    description: Optional[str],
    db: Session,
    user_id: int,
) -> int:
    if category_id is not None:
        return category_id

    if not description:
        raise HTTPException(
            status_code=400,
            detail="category_id is required when description is not provided"
        )

    user_categories = db.query(Category).filter(Category.user_id == user_id).all()
    category_names = [c.name for c in user_categories]

    predicted_name = categorize(description, category_names)

    if predicted_name is None:
        raise HTTPException(
            status_code=400,
            detail="Could not determine category automatically. Please specify category_id explicitly."
        )

    category = db.query(Category).filter(
        Category.name == predicted_name,
        Category.user_id == user_id
    ).first()

    return category.id