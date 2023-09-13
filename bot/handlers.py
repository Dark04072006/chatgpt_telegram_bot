"""
Модуль хэндлеров
"""
import os
import dotenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.chatgpt import ChatGPT

dotenv.load_dotenv(".env")

router = Router()
chatgpt = ChatGPT(os.getenv("OPENAI_API_TOKEN"))


def group_command_filter(message: Message) -> bool:
    """Фильтр сообщений в группе"""
    return message.text.startswith("/gpt") and message.chat.type in (
        "group",
        "supergroup",
    )


@router.message(Command("start"))
async def start_command_handler(message: Message) -> None:
    """Команда запуска бота"""
    await message.reply("Приветствую! Задай запрос, на который бот должен ответить.")


@router.message(Command("clean"))
async def clean_session_handler(message: Message) -> None:
    """Команда очистки сессии пользователя"""
    chatgpt.drop_messages(message.from_user.id)
    await message.reply("Сессия удалена")


@router.message(F.chat.type == "private")
async def text_handler(message: Message) -> None:
    """Основной обработчик сообщений"""
    msg = await message.reply("Обработка запроса...")
    response = chatgpt.create_completion(message.text, message.from_user.id)
    await message.bot.edit_message_text(response, message.chat.id, msg.message_id)


@router.message(lambda message: group_command_filter(message=message))
async def group_message_handler(message: Message) -> None:
    """Обработчик команды /gpt в группе"""
    message_ = await message.reply("Обработка запроса...")
    prompt = message.text.strip("/gpt").strip()
    response = chatgpt.create_completion(prompt, message.from_user.id)
    await message_.edit_text(response)
