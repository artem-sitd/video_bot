import asyncio
from aiogram import types
from llm.client import parse_user_query
from llm.schemas import ParsedQuery
from services.dispatcher import dispatch

# единый обработчик ТГ запросов от пользователя
async def handle_message(message: types.Message):
    user_text = message.text
    loop = asyncio.get_running_loop()

    try:
        llm_response = await loop.run_in_executor(
            None, parse_user_query, user_text)
        parsed = ParsedQuery.model_validate_json(llm_response)
    except Exception as e:
        print(e)
        await message.answer("Не смог понять запрос")
        return

    result = await dispatch(parsed)
    await message.answer(str(result))
