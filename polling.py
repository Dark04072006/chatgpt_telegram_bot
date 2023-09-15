"""файл в котором проходит инициализация бота и запуск поллинга"""

import os
import asyncio
import logging
import dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import router
from bot.middlewares.subscribe import SubscribeMiddleware


async def on_startup(bot: Bot) -> None:
    """Функция которая отрабатывает перед запуском бота"""
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="clean", description="Очистка сессии пользователя"),
            BotCommand(command="help", description="Помощь"),
        ]
    )
    await bot.delete_webhook(drop_pending_updates=True)


async def main() -> None:
    """Инициализация всех компонентов бота"""

    dotenv.load_dotenv(".env")

    dispatcher = Dispatcher()

    dispatcher.startup.register(on_startup)
    dispatcher.include_router(router)
    dispatcher.message.middleware(SubscribeMiddleware())

    bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.close()
