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
    "🚘 Inomarka": [
        "Malibu 2", "Tracker 2", "Kia K5", "BMW X5",
        "Cherry 7 pro", "Cherry 8 pro max", "Bugatti", "Onix",
        "Toyota Camry", "Hyundai Sonata", "BYD Song Plus", "Zeekr 001",
        "Mercedes G63", "Lexus LX 600", "Equinox", "Tahoe",
    ],
    "🚗 Oddiy mashinalar": [
        "Cobalt", "Gentra", "Spark", "Damas",
        "Nexia 2", "07", "06", "Matiz",
        "Nexia 3", "Lacetti", "Labo", "Tico",
    ],
}

MASHINA_NARXLARI = {
    # Inomarkalar
    "Malibu 2": 420_000_000,
    "Tracker 2": 290_000_000,
    "Kia K5": 450_000_000,
    "BMW X5": 950_000_000,
    "Cherry 8 pro max": 200_000_000,
    "Cherry 7 pro": 210_000_000,
    "Bugatti": 20_000_000_000,
    "Onix": 169_000_000,
    "Toyota Camry": 520_000_000,
    "Hyundai Sonata": 430_000_000,
    "BYD Song Plus": 395_000_000,
    "Zeekr 001": 650_000_000,
    "Mercedes G63": 3_200_000_000,
    "Lexus LX 600": 2_400_000_000,
    "Equinox": 440_000_000,
    "Tahoe": 1_150_000_000,

    # Oddiy mashinalar
    "Cobalt": 155_000_000,
    "Gentra": 175_000_000,
    "Spark": 59_000_000,
    "Damas": 90_000_000,
    "Nexia 2": 75_000_000,
    "07": 50_000_000,
    "06": 45_000_000,
    "Matiz": 48_000_000,
    "Nexia 3": 125_000_000,
    "Lacetti": 145_000_000,
    "Labo": 95_000_000,
    "Tico": 32_000_000,
}

RANGLAR = [
    "⚪️ Oq", "⚫️ Qora", "🔘 Mokriy asfalt", "🥈 Kumushrang",
    "👌Sariq", "❤️Qizil", "🔵 Ko'k", "🟢 Yashil",
    "🟤 Jigarrang", "🟠 To'q sariq", "🟣 Binafsha", "🩶 Kulrang",
]

NOMER_NARXLARI = {
    "60 A 777 AA": 15_000_000,
    "40 Z 777 ZZ": 1_000_000_000,
    "01 A 001 AA": 25_000_000,
    "50 Y 100 UZ": 8_000_000,
    "70 K 430 JA":3_800_000,
    "10 B 111 OY ":9_000_000,
    "40 B 888 BB":999_999_999,
    "40 K 999 BR":25_000_000,
}
ODDIY_NOMER_NARXI = 3_000_000


def fmt_sum(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " so'm"


def togri_raqammi(text: str) -> bool:
    cleaned = re.sub(r"\s+", "", text.upper())
    return bool(re.fullmatch(r"(?:\d{2})?[A-Z]\d{3}[A-Z]{2}|\d{3}[A-Z]{3}", cleaned))


def parse_pul(text: str) -> int | None:
    cleaned = text.replace(" ", "").replace(",", "").replace(".", "")
    if not cleaned.isdigit():
        return None
    val = int(cleaned)
    return val if val > 0 else None


def togri_telmi(text: str) -> bool:
    digits = re.sub(r"\D", "", text)
    return len(digits) in (9, 12)


@router.message(CommandStart())
async def start(m: types.Message, state: FSMContext):
    await state.clear()
    await m.answer("Assalomu aleykum hurmatli mijoz:", reply_markup=kb(["🚘 Inomarka", "🚗 Oddiy mashinalar"]))
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

    car_price = MASHINA_NARXLARI[m.text]
    await state.update_data(nomi=m.text, car_price=car_price)
    rows = [RANGLAR[i : i + 2] for i in range(0, len(RANGLAR), 2)]
    await m.answer(
        f"{m.text} summasi: {fmt_sum(car_price)}\nEndi rangini tanlang:",
        reply_markup=kb(*rows),
    )
    await state.set_state(Form.rangi)


@router.message(Form.rangi)
async def rangi(m: types.Message, state: FSMContext):
    if m.text not in RANGLAR:
        return await m.answer("Rangni pastdagi tugmalardan tanlang!")
    await state.update_data(rangi=m.text)
    await m.answer("Nomer tanlang yoki yozing:", reply_markup=kb(["🔢 Nomerlar"]))
    await state.set_state(Form.raqami)


@router.message(Form.raqami)
async def raqami(m: types.Message, state: FSMContext):
    if m.text == "🔢 Nomerlar":
        nomer_list = list(NOMER_NARXLARI.keys())
        rows = [nomer_list[i : i + 2] for i in range(0, len(nomer_list), 2)]
        info = "\n".join(f"• {k} — {fmt_sum(v)}" for k, v in NOMER_NARXLARI.items())
        return await m.answer(f"Nomerlardan birini tanlang:\n\n{info}", reply_markup=kb(*rows))

    if not m.text or not togri_raqammi(m.text):
        return await m.answer("Raqam noto'g'ri! Qayta kiriting yoki '🔢 Nomerlar' tugmasini bosing:")

    raqam_clean = m.text.upper().strip()
    nomer_price = NOMER_NARXLARI.get(raqam_clean, ODDIY_NOMER_NARXI)
    d = await state.get_data()
    jami = d["car_price"] + nomer_price

    await state.update_data(raqami=raqam_clean, nomer_price=nomer_price, jami=jami)
    await m.answer(
        f"Nomer summasi: {fmt_sum(nomer_price)}\n"
        f"Mashina + nomer jami summasi: {fmt_sum(jami)}\n\n"
        f"Byudjetingiz (pulingiz) qancha? (Faqat raqamda yozing):",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Form.puli)


@router.message(Form.puli)
async def puli(m: types.Message, state: FSMContext):
    amount = parse_pul(m.text or "")
    if amount is None:
        return await m.answer("Pulni noto'g'ri kiritdingiz! Faqat raqam bilan qayta kiriting:")

    d = await state.get_data()
    if amount < d["jami"]:
        return await m.answer(
            f"Mablag' yetarli emas!\n"
            f"Jami summa: {fmt_sum(d['jami'])}\n"
            f"Siz kiritgan summa: {fmt_sum(amount)}\n"
            f"Yetarli summani qayta kiriting:"
        )

    await state.update_data(puli=fmt_sum(amount))
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
        f"Nomi: {d['nomi']} ({fmt_sum(d['car_price'])})\n"
        f"Rangi: {d['rangi']}\n"
        f"Raqami: {d['raqami']} ({fmt_sum(d['nomer_price'])})\n"
        f"Jami summa: {fmt_sum(d['jami'])}\n"
        f"Sizning byudjetingiz: {d['puli']}\n"
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

