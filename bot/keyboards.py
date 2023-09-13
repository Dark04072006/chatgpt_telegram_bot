from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def regenerate_response_button() -> InlineKeyboardMarkup:
    """
    Кнопка регенерации ответа ИИ
    """
    text = "regenerate response"
    button = [InlineKeyboardButton(text=text, callback_data="regenerate")]
    return InlineKeyboardMarkup(inline_keyboard=[button])
