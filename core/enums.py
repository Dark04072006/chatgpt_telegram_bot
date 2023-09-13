from enum import Enum


class RoleEnum(Enum):
    """
    Enum ролей сообщения
    """
    SYSTEM: str = "system"
    USER: str = "user"
    ASSISTANT: str = "assistant"
