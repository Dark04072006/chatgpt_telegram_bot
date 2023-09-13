from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SubscribeMiddleware(BaseMiddleware):
    """Middleware перехватывающее все входящие
    updates и проверяет на то подписан ли юзер на канал"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        member = await event.bot.get_chat_member(
            "@time_to_learn_python_channel", event.from_user.id
        )
        if not member.status in (
            "member",
            "owner",
            "administrator",
            "creator",
        ) and member.user.first_name not in ("Channel", "Group", "SuperGroup"):
            await event.bot.send_message(
                chat_id=event.chat.id,
                text="Чтобы использовать ИИ - подпишитесь на наш канал",
                reply_to_message_id=event.message_id,
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Подписаться!",
                                url="https://t.me/time_to_learn_python_channel",
                            )
                        ]
                    ]
                ),
            )
        else:
            return await handler(event, data)
