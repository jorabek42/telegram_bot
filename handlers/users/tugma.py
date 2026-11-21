from aiogram import F, Router, filters, types
from keyboads.tugma_reply import tugma

rt = Router()



@rt.message(filters.Command("tugma"))
async def tugma_handler(msg: types.Message):
    await msg.answer("xohlagan tugmangizni tanlang", reply_markup=tugma())


@rt.message()
async def tugma_handler2(msg: types.Message):
    data = msg.chat_shared
    print(data)

    kanal_id = data.chat_id
    title = data.title or "Nomi yo'q"
    username = (data.username and f"@{data.username}") or "Yo'q"
    rasm = data.photo and data.photo[-1].file_id

    n = (
        f"kanal id: {kanal_id}\n"
        f"title: {title}\n"
        f"username: {username}"
    )
    await msg.answer(n)
    rasm and await msg.answer_photo(rasm)


@rt.message(F.chat_shared.request_id == 7075)
async def tugma_handler3(msg: types.Message):
    data = msg.chat_shared
    print(data)

    guruh_id = data.chat_id
    title = data.title or "Nomi yo'q"
    username = (data.username and f"@{data.username}") or "Yo'q"
    rasm = data.photo and data.photo[-1].file_id

    n = (
        f"guruh id: {guruh_id}\n"
        f"title: {title}\n"
        f"username: {username}"
    )
    await msg.answer(n)
    rasm and await msg.answer_photo(rasm)