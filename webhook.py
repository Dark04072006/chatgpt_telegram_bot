"""файл в котором проходит инициализация бота и запуск webhook"""

import os
import logging
import dotenv
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
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
    await bot.set_webhook(url=os.getenv("WEBHOOK_URL") + "/webhook")


def main():
    """Инициализация всех компонентов бота"""

    dotenv.load_dotenv(".env")

    dispatcher = Dispatcher()

    dispatcher.startup.register(on_startup)
    dispatcher.include_router(router)
    dispatcher.message.middleware(SubscribeMiddleware())

    app = web.Application()

    bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))

    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path="/webhook")

    setup_application(app, dispatcher, bot=bot)

    web.run_app(app)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
