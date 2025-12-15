import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import settings
from bot.handlers import handle_message


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message):
        await message.answer(
            "Привет! Я бот аналитики по видео.\n"
            "Задай вопрос на русском языке."
        )

    @dp.message()
    async def message_handler(message: Message):
        await handle_message(message)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
