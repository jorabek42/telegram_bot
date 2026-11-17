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
    b.button(text="gurpa yoki bot", request_chat=KeyboardButtonRequestChat(
        request_id=4396,
        user_is_premium=False,
    ))
    b.button(text="user yoki bot", request_users=KeyboardButtonRequestUsers(
        request_id=425,
        user_is_bot=True
    ))
    b.button(text="kanal yoki gurpa", request_chat=KeyboardButtonRequestChat(
        request_id=4236,
        chat_is_channel=True,

    ))

    b.button(text="kanal yoki gurpa", request_chat=KeyboardButtonRequestChat(
        request_id=4396,
        chat_is_forum=False,
    ))
    b.button(text="kanal yoki gurpa", request_chat=KeyboardButtonRequestChat(
        request_id=906,
        chat_has_username=True,
    ))
    b.button(text="kanal yoki gurpa", request_chat=KeyboardButtonRequestChat(
        request_id=9069,
        bot_is_member=False,
    ))




    b.adjust(3)
    return b.as_markup(resize_keyboard=True)
