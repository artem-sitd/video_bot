from openai import OpenAI
from config import settings
from .prompt import SYSTEM_PROMPT
import traceback
import httpx

# прокси для openai,
proxy_url = settings.get_proxy_url

http_client = httpx.Client(
    proxy=proxy_url,
    timeout=30.0,
)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    http_client=http_client,
)


class ApiCounter:
    def __init__(self):
        self.count = 0


counter = ApiCounter()


# отправка промпта + сообщения от пользователя по апи openai
# и получение готовой правивальной json схемы
def parse_user_query(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0,
        )

        # для отладки!
        counter.count += 1
        print(f"{counter.count}. OPENAI RESPONSE:", response)
        return response.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", e)
        traceback.print_exc()
        raise
