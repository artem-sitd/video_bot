from aiogram import types
from llm.client import parse_user_query
from llm.schemas import ParsedQuery
from services.dispatcher import dispatch


async def handle_message(message: types.Message):
    user_text = message.text

    llm_response = parse_user_query(user_text)

    try:
        parsed = ParsedQuery.model_validate_json(llm_response)
    except Exception:
        await message.answer("Не смог понять запрос")
        return

    result = dispatch(parsed)
    await message.answer(str(result))
