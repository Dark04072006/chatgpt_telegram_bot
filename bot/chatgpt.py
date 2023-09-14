import openai
import json
from core.patterns import Singleton


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

        # Загрузка существующих сессий из файла sessions.json
        try:
            with open("sessions.json", "r", encoding="utf-8") as file:
                self.sessions = json.load(file)
        except FileNotFoundError:
            pass

    def create_session(self, session_id: int) -> None:
        """
        Создает новую сессию для взаимодействия с ChatGPT.

        Args:
            session_id (int): Идентификатор сессии.
        """
        self.sessions[session_id] = {"messages": []}
        with open("sessions.json", "w", encoding="utf-8") as file:
            json.dump(self.sessions, file, indent=2, ensure_ascii=False)

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
        with open("sessions.json", "w", encoding="utf-8") as file:
            json.dump(self.sessions, file, ensure_ascii=False, indent=2)

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
            with open("sessions.json", "w", encoding="utf-8") as file:
                json.dump(self.sessions, file, ensure_ascii=False, indent=2)

    def change_default_message_settings(self, content: str, session_id: int) -> None:
        """
        Изменяет системные настройки ChatGPT.

        Args:
            content (str): Новые системные настройки.
            session_id (int): Идентификатор сессии.
        """
        self.update_messages("system", content, session_id)
        with open("sessions.json", "w", encoding="utf-8") as file:
            json.dump(self.sessions, file, ensure_ascii=False, indent=2)
