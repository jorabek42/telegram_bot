import asyncio
import re
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

router = Router()


class Form(StatesGroup):
    turi = State()
    nomi = State()
    rangi = State()
    raqami = State()
    puli = State()
    tel = State()


def kb(*rows, contact=False):
    keyboard = [
        [KeyboardButton(text=t, request_contact=contact if i == 0 and j == 0 else False) for j, t in enumerate(row)]
        for i, row in enumerate(rows)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


TURLAR = {
    "🚘 Inomarka": ["Malibu 2", "Tracker 2", "Kia K5", "BMW X5"],
    "🚗 Oddiy mashinalar": ["Cobalt", "Gentra", "Onix", "Damas"],
}
RANGLAR = ["⚪️ Oq", "⚫️ Qora", "🔘 Mokriy asfalt", "🥈 Kumushrang"]


def togri_raqammi(text: str) -> bool:
    # Masalan: 01 A 777 AA, 01A777AA yoki 777AAA formatini tekshiradi
    cleaned = re.sub(r"\s+", "", text.upper())
    return bool(re.fullmatch(r"(?:\d{2})?[A-Z]\d{3}[A-Z]{2}|\d{3}[A-Z]{3}", cleaned))


def togri_pulmi(text: str) -> bool:
    cleaned = text.replace(" ", "").replace(",", "").replace(".", "")
    return cleaned.isdigit() and int(cleaned) > 0


def togri_telmi(text: str) -> bool:
    digits = re.sub(r"\D", "", text)
    return len(digits) in (9, 12)


@router.message(CommandStart())
async def start(m: types.Message, state: FSMContext):
    await state.clear()
    await m.answer("Bo'limni tanlang:", reply_markup=kb(["🚘 Inomarka", "🚗 Oddiy mashinalar"]))
    await state.set_state(Form.turi)


@router.message(Form.turi)
async def turi(m: types.Message, state: FSMContext):
    if m.text not in TURLAR:
        return await m.answer("Tugmadan tanlang.")
    await state.update_data(turi=m.text)
    cars = TURLAR[m.text]
    rows = [cars[i : i + 2] for i in range(0, len(cars), 2)] + [["⬅️ Orqaga"]]
    await m.answer("Mashina nomini tanlang:", reply_markup=kb(*rows))
    await state.set_state(Form.nomi)


@router.message(Form.nomi)
async def nomi(m: types.Message, state: FSMContext):
    if m.text == "⬅️ Orqaga":
        return await start(m, state)
    turi_val = (await state.get_data()).get("turi")
    if m.text not in TURLAR.get(turi_val, []):
        return await m.answer("Mashina nomini tugmadan tanlang.")
    await state.update_data(nomi=m.text)
    rows = [RANGLAR[i : i + 2] for i in range(0, len(RANGLAR), 2)]
    await m.answer("Rangini tanlang:", reply_markup=kb(*rows))
    await state.set_state(Form.rangi)


@router.message(Form.rangi)
async def rangi(m: types.Message, state: FSMContext):
    if m.text not in RANGLAR:
        return await m.answer("Rangni pastdagi tugmalardan tanlang!")
    await state.update_data(rangi=m.text)
    await m.answer("Mashina raqamini yozing (masalan: 01 A 777 AA):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.raqami)


@router.message(Form.raqami)
async def raqami(m: types.Message, state: FSMContext):
    if not m.text or not togri_raqammi(m.text):
        return await m.answer("Raqam noto'g'ri! Qayta kiriting (masalan: 01 A 777 AA):")
    await state.update_data(raqami=m.text.upper())
    await m.answer("Puli (byudjeti) qancha? (Faqat raqamda yozing, masalan: 250000000)")
    await state.set_state(Form.puli)


@router.message(Form.puli)
async def puli(m: types.Message, state: FSMContext):
    if not m.text or not togri_pulmi(m.text):
        return await m.answer("Pulni noto'g'ri kiritdingiz! Faqat raqam bilan qayta kiriting:")
    await state.update_data(puli=m.text.strip())
    await m.answer("Telefon raqamingizni yuboring:", reply_markup=kb(["📱 Raqamni yuborish"], contact=True))
    await state.set_state(Form.tel)


@router.message(Form.tel)
async def tel(m: types.Message, state: FSMContext):
    if m.contact:
        phone = m.contact.phone_number
    elif m.text and togri_telmi(m.text):
        phone = m.text.strip()
    else:
        return await m.answer("Telefon raqamini noto'g'ri kiritdingiz! Qayta kiriting yoki tugmani bosing:")

    d = await state.get_data()
    await state.clear()
    await m.answer(
        f"Siz muvaffaqiyatli mashina oldingiz! Aloqaga chiqamiz.\n\n"
        f"Turi: {d['turi']}\n"
        f"Nomi: {d['nomi']}\n"
        f"Rangi: {d['rangi']}\n"
        f"Raqami: {d['raqami']}\n"
        f"Puli: {d['puli']}\n"
        f"Telefon: {phone}",
        reply_markup=ReplyKeyboardRemove(),
    )


async def main():
    bot = Bot(token="TOKENNI_SHU_YERGA_QOYING")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())