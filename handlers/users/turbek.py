from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.tur_states   import TurState
from keyboards.tur_keyboards import (
    tur_transport,
    tur_transport_darajasi,
    tur_qaytish,
    tur_manzil,
    tur_nomer,
    transport, transport_darajasi, manzil, qaytish
)
rt = Router()
@rt.message(filters.Command("start"))
async def tur_handler(msg: types.Message, state: FSMContext):
    await msg.answer(f"{msg.from_user.first_name} sizni ko'rganimizdan xursandmiz")
    await msg.answer("transport turini tanlang", reply_markup=tur_transport())
    await state.set_state(TurState.transport)
@rt.message(TurState.transport)
async def transport_handler(msg: types.Message, state: FSMContext):
    if msg.text in transport:
        await msg.answer("transportning qanday darajasini tanlaysiz", reply_markup=tur_transport_darajasi())
        await state.set_state(TurState.transport_darajasi)
        await state.update_data(transport=msg.text)
    else:
        await msg.answer("transport turini to'g'ri tanlang!")
        await state.set_state(TurState.transport)
@rt.message(TurState.transport_darajasi)
async def transport_darajasi_handler(msg: types.Message, state: FSMContext):
    await msg.answer("qaytasizmi yoki qaytmesizmi?", reply_markup=tur_qaytish())
    await state.set_state(TurState.qaytish)
    await state.update_data(transport_darajasi=msg.text)
@rt.message(TurState.qaytish)
async def qaytish_handler(msg: types.Message, state: FSMContext):
    await msg.answer("manzil kiriting", reply_markup=tur_manzil())
    await state.set_state(TurState.manzil)
    await state.update_data(qaytish=msg.text)
@rt.message(TurState.manzil)
async def manzil_handler(msg: types.Message, state: FSMContext):
    await msg.answer("aloqaga chiqish uchun nomer bering", reply_markup=tur_nomer())
    await state.set_state(TurState.nomer)
    await state.update_data(manzil=msg.text)
@rt.message(TurState.nomer)
async def nomer_handler(msg: types.Message, state: FSMContext):
    await msg.answer("barcha malumotlaringiz qabul qilindi tez orada aloqaga chiqamiz!", reply_markup=ReplyKeyboardRemove())
    await state.update_data(nomer=msg.text)
    data = await state.get_data()
    await state.clear()
    await msg.answer(str(data))
