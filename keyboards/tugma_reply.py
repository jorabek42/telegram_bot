from aiogram.types import (
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUsers,
    WebAppInfo,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def tugma():
    b = ReplyKeyboardBuilder()
    b.button(
        text="channel",
        request_chat=KeyboardButtonRequestChat(
            request_id=11111,
            chat_is_channel=True,
            request_title=True,
            request_username=True,
            request_photo=True,
        ),
    )
    b.button(
        text="Guruh",
        request_chat=KeyboardButtonRequestChat(
            request_id=7075,
            chat_is_channel=False,
            request_title=True,
            request_username=True,
            request_photo=True,
        ),
    )

    b.button(text="Text")
    b.button(text="Phone Number", request_contact=True)
    b.button(text="Location", request_location=True)
    b.button(text="YouTube", web_app=WebAppInfo(url="https://www.youtube.com/"))
    b.button(
        text="Bot",
        request_users=KeyboardButtonRequestUsers(
            request_id=1,
            user_is_bot=True,
            max_quantity=1
        ),
    )
    b.button(
        text="Botlar",
        request_users=KeyboardButtonRequestUsers(
            request_id=11,
            user_is_bot=True,
            max_quantity=10
        ),
    )
    b.button(
        text="Foydalanuvchi",
        request_users=KeyboardButtonRequestUsers(
            request_id=2,
            user_is_bot=False,
            max_quantity=1
        ),
    )
    b.button(
        text="Foydalanuvchilar",
        request_users=KeyboardButtonRequestUsers(
            request_id=12,
            user_is_bot=False,
            max_quantity=10
        ),
    )
    b.button(
        text="Kanallar",
        request_chat=KeyboardButtonRequestChat(
            request_id=13,
            chat_is_channel=True,
            max_quantity=10
        ),
    )
    b.button(
        text="Guruhlar",
        request_chat=KeyboardButtonRequestChat(
            request_id=14,
            chat_is_channel=False,
            max_quantity=10
        ),
    )

    b.adjust(3)
    return b.as_markup(resize_keyboard=True)