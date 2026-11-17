from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def tugma() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    b.button(text="Claude", url="https://claude.ai")
    b.button(text="Gemini", url="https://gemini.google.com")
    b.button(text="ChatGPT", url="https://chatgpt.com")

    b.adjust(3)
    return b.as_markup()