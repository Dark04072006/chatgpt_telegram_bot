import openai


class Singleton(type):
    """Синглтон реализация"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ChatGPT:
    """Класс для работы с API ChatGPT"""

    __metaclass__ = Singleton

    def __init__(self, api_key: str) -> None:
        """
        Инициализирует объект ChatGPT с указанным API ключом.

        Args:
            api_key (str): API ключ для доступа к OpenAI API.
        """
        self.api_key = api_key
        self.sessions = {}

    def create_session(self, session_id: int) -> None:
        """
        Создает новую сессию для взаимодействия с ChatGPT.

        Args:
            session_id (int): Идентификатор сессии.
        """
        self.sessions[session_id] = {"messages": []}

    def update_messages(self, role: str, content: str, session_id: int) -> None:
        """
        Добавляет сообщение в текущую сессию.

        Args:
            role (str):
                Роль отправителя сообщения ('user', 'assistant', 'system').
            content (str): Содержание сообщения.
            session_id (int): Идентификатор сессии, к которой добавляется сообщение.
        """
        if session_id not in self.sessions:
            self.create_session(session_id)
        self.sessions[session_id]["messages"].append({"role": role, "content": content})

    def create_completion(self, content: str, session_id: int) -> str:
        """
        Создает запрос на генерацию ответа от ChatGPT на основе
        предоставленного контента.

        Args:
            content (str): Входной текст, который передается ChatGPT.
            session_id (int): Идентификатор сессии.

        Returns:
            str: Сгенерированный ответ от ChatGPT.
        """
        self.update_messages("user", content, session_id)
        messages = self.sessions.get(session_id, {}).get("messages", [])
        response = openai.ChatCompletion.create(
            messages=messages,
            model="gpt-3.5-turbo-16k",
            api_key=self.api_key,
        )
        result = response["choices"][0]["message"]["content"]
        self.update_messages("assistant", result, session_id)
        return result

    def drop_messages(self, session_id: int) -> None:
        """
        Удаляет сообщения пользователя из текущей сессии.

        Args:
            session_id (int): Идентификатор сессии.
        """
        if session_id in self.sessions:
            self.sessions[session_id]["messages"] = []

    def change_default_message_settings(self, content: str, session_id: int) -> None:
        """
        Изменяет системные настройки ChatGPT.

        Args:
            content (str): Новые системные настройки.
            session_id (int): Идентификатор сессии.
        """
        self.update_messages("system", content, session_id)