from aiogram.filters import BaseFilter
from aiogram.types import Message


class GroupCommandFilter(BaseFilter):
    """Фильтр обработки комманд в группе"""

    def __init__(self, command: str = "/", *, admin: bool = False) -> None:
        self.chat_type = ["group", "supergroup"]
        self.admin = admin
        self.command = command

    async def __call__(self, message: Message) -> bool:
        if message.chat.type in self.chat_type:
            if message.text.startswith(self.command):
                if self.admin:
                    try:
                        member = await message.bot.get_chat_member(
                            message.chat.id, message.from_user.id
                        )
                        print(member)
                        return member.status in (
                            "owner",
                            "administrator",
                            "creator",
                        ) or member.user.username in (
                            "Channel_Bot",
                            "GroupAnonymousBot",
                        )
                    except AttributeError:
                        return False
                return True
