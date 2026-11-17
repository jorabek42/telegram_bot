from aiogram.types import (
    InlineKeyboardMarkup,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def tugma():
    b = ReplyKeyboardBuilder()
    b.button(text="user yoki bot", request_users=KeyboardButtonRequestUsers(
        request_id=435,
        user_is_bot=False,
    ))
    b.button(text="user yoki bot", request_users=KeyboardButtonRequestUsers(
        request_id=425,
        user_is_bot=True
    ))
    b.button(text="kanal", request_chat=KeyboardButtonRequestChat(
        request_id=4236,
        chat_is_channel=True,
    ))
    b.button(text="gurpa", request_chat=KeyboardButtonRequestChat(
        request_id=42236,
        chat_is_channel=False,
    ))
    b.button(text="gurpa", request_chat=KeyboardButtonRequestChat(
        request_id=436,
        chat_is_channel=True,
    ))


    b.adjust(3)
    return b.as_markup(resize_keyboard=True)
