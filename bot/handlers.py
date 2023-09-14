"""
Модуль хэндлеров
"""
import os
import random
from datetime import timedelta
import dotenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from bot.chatgpt import ChatGPT
from bot.filters import GroupCommandFilter


dotenv.load_dotenv(".env")

router = Router()
chatgpt = ChatGPT(os.getenv("OPENAI_API_TOKEN"))


@router.message(Command("start"))
async def start_command_handler(message: Message) -> None:
    """Команда запуска бота"""
    await message.reply("Приветствую! Задай запрос, на который бот должен ответить.")


@router.message(Command("clean"))
async def clean_session_handler(message: Message) -> None:
    """Команда очистки сессии пользователя"""
    chatgpt.drop_messages(str(message.from_user.id))
    await message.reply("Сессия удалена")


@router.message(F.chat.type == "private")
async def text_handler(message: Message) -> None:
    """Основной обработчик сообщений"""
    msg = await message.reply("Обработка запроса...")
    response = chatgpt.create_completion(message.text, message.from_user.id)
    await message.bot.edit_message_text(
        response, str(message.from_user.id), msg.message_id
    )


@router.message(GroupCommandFilter("/gpt"))
async def group_message_handler(message: Message) -> None:
    """Обработчик команды /gpt в группе"""
    message_ = await message.reply("Обработка запроса...")
    prompt = message.text.strip("/gpt").strip()
    response = chatgpt.create_completion(prompt, str(message.from_user.id))
    await message_.edit_text(response)


@router.message(GroupCommandFilter("/set"))
async def set_chatgpt_settings_handler(message: Message) -> None:
    """Смена настроек ИИ"""
    text = message.text.strip("/set").strip()
    chatgpt.change_default_message_settings(text, str(message.from_user.id))
    await message.reply("Стандартная настройка изменена.")


@router.message(GroupCommandFilter("/mute", admin=True))
async def mute_user_handler(message: Message) -> None:
    """Функция мута пользователя"""
    try:
        user_id = message.reply_to_message.from_user.id
        mute_time = int(message.text.split()[1])
        await message.bot.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=mute_time),
        )

        await message.reply(
            f"Пользователю: {message.reply_to_message.from_user.full_name}"
            + " "
            + "ограничена отправка сообщений на "
            + str(mute_time)
            + " часов"
        )

    except AttributeError:
        await message.reply("Эта команда должна быть ответом на сообщение.")


@router.message(GroupCommandFilter("!инфа"))
async def random_value_handler(message: Message) -> None:
    """Обработчик команды !инфо"""
    await message.reply(
        f"{message.from_user.full_name}, вероятность составляет - {random.randint(1, 100)}%"
    )


@router.message(Command("help"))
async def help_command_handler(message: Message) -> None:
    """Обработчик списка команд"""
    await message.reply(
        "Список команд:\n"
        + "/start - запуск бота\n"
        + "/clean - очистить сессию ИИ\n"
        + "Команды для групп:\ngpt {ваш запрос к ИИ}\nset {ваша настройка ИИ}\n!инфо {ваше условие}"
    )
