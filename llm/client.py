from openai import OpenAI
from config import settings
from prompt import SYSTEM_PROMPT

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def parse_user_query(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0,
    )
    return response.choices[0].message.content
