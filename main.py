"""Основной файл в котором проходит инициализация бота"""

import os
import asyncio
import dotenv
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import router
from bot.middlewares.subscribe import SubscribeMiddleware


async def main():
    """Инициализация всех компонентов бота"""
    logging.basicConfig(level=logging.INFO)

    dotenv.load_dotenv(".env")

    bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="clean", description="Очистка сессии пользователя"),
            BotCommand(command="help", description="Помощь"),
        ]
    )
    dispatcher = Dispatcher()

    dispatcher.message.middleware(SubscribeMiddleware())
    dispatcher.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
