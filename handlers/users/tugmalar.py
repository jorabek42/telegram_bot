
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

rt = Router()

@rt.message(CommandStart("get"))
async def get_id(message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Select user")],
            [KeyboardButton(text="Select channel"),KeyboardButton(text="Select group chat")],  [KeyboardButton(text="Select bot")] ], resize_keyboard=True)

    await message.answer(f"Your ID: {user_id}\n"  f"Current chat ID: {chat_id}",  reply_markup=keyboard )


@rt.message(F.text == "Select user")
async def select_user(message: Message):
    await message.answer("User tanlash uchun foydalanuvchi ID raqamini yuboring.")


@rt.message(F.text == "Select channel")
async def select_channel(message: Message):
    await message.answer("Kanal ID raqamini yuboring.")


@rt.message(F.text == "Select group chat")
async def select_group(message: Message):
    await message.answer("Guruh ID raqamini yuboring.")


@rt.message(F.text == "Select bot")
async def select_bot(message: Message):
    await message.answer("Bot username yuboring.")
