import httpx

from app.core.config import get_settings

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