import asyncio
from aiogram import types
from llm.client import parse_user_query
from llm.schemas import QueryPlan
from services.dispatcher import dispatch_query
from services.clean_response import extract_json

# единый обработчик ТГ запросов от пользователя
async def handle_message(message: types.Message):
    user_text = message.text
    print()
    print(f'юзер спрашивает >>: {user_text}')
    loop = asyncio.get_running_loop()

    try:
        llm_response = await loop.run_in_executor(
            None, parse_user_query, user_text)

        cleaned_resp = extract_json(llm_response)
        parsed = QueryPlan.model_validate_json(cleaned_resp)
    except Exception as e:
        print(e)
        await message.answer("Не смог понять запрос")
        return

    result = await dispatch_query(parsed)
    await message.answer(str(result))
