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

MASHINA_RASMLARI = {
    "Malibu 2": "https://upload.wikimedia.org/wikipedia/commons/4/41/Chevrolet_Malibu_Premier_2.0T_%282019%29.jpg",
    "Tracker 2": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Chevrolet_Tracker_RS_%28China%29.jpg",
    "Kia K5": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Kia_K5_DL3_black_%281%29.jpg",
    "BMW X5": "https://upload.wikimedia.org/wikipedia/commons/1/1d/2019_BMW_X5_xDrive40i_M_Sport_3.0.jpg",
    "Cherry 8 pro max": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Chery_Tiggo_8_Pro_Max_01.jpg",
    "Cherry 7 pro": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Chery_Tiggo_7_Pro_01.jpg",
    "Bugatti": "https://upload.wikimedia.org/wikipedia/commons/4/45/Bugatti_Chiron_Pur_Sport_at_Geneva_Motor_Show_2019.jpg",
    "Onix": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Chevrolet_Onix_sedan_China.jpg",
    "Toyota Camry": "https://upload.wikimedia.org/wikipedia/commons/a/ac/2018_Toyota_Camry_XSE_%28front%29.jpg",
    "Hyundai Sonata": "https://upload.wikimedia.org/wikipedia/commons/6/6f/2020_Hyundai_Sonata_Limited_%28front%29.jpg",
    "BYD Song Plus": "https://upload.wikimedia.org/wikipedia/commons/5/59/BYD_Song_Plus_DM-i_front.jpg",
    "Zeekr 001": "https://upload.wikimedia.org/wikipedia/commons/9/96/Zeekr_001_001.jpg",
    "Mercedes G63": "https://upload.wikimedia.org/wikipedia/commons/1/15/Mercedes-AMG_G63_IMG_4263.jpg",
    "Lexus LX 600": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Lexus_LX_600_F_SPORT_001.jpg",
    "Equinox": "https://upload.wikimedia.org/wikipedia/commons/7/7c/2018_Chevrolet_Equinox_Premier_%28front%29.jpg",
    "Tahoe": "https://upload.wikimedia.org/wikipedia/commons/4/44/2021_Chevrolet_Tahoe_RST.jpg",

    "Cobalt": "https://upload.wikimedia.org/wikipedia/commons/9/99/Chevrolet_Cobalt_sedan_Brazil.jpg",
    "Gentra": "https://upload.wikimedia.org/wikipedia/commons/8/87/Chevrolet_Lacetti_sedan_front.jpg",
    "Spark": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Chevrolet_Spark_M300_front.jpg",
    "Damas": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Suzuki_Every_DA64V_01.jpg",
    "Nexia 2": "https://upload.wikimedia.org/wikipedia/commons/6/63/Daewoo_Nexia_sedan_front.jpg",
    "07": "https://upload.wikimedia.org/wikipedia/commons/4/42/VAZ-2107_Lada_Riva.jpg",
    "06": "https://upload.wikimedia.org/wikipedia/commons/1/12/VAZ-2106_Lada_1600.jpg",
    "Matiz": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Daewoo_Matiz_front.jpg",
    "Nexia 3": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Chevrolet_Aveo_T250_sedan_front.jpg",
    "Lacetti": "https://upload.wikimedia.org/wikipedia/commons/8/87/Chevrolet_Lacetti_sedan_front.jpg",
    "Labo": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Suzuki_Every_DA64V_01.jpg",
    "Tico": "https://upload.wikimedia.org/wikipedia/commons/6/64/Daewoo_Tico_SX_front.jpg",
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
    "70 K 430 JA": 3_800_000,
    "10 B 111 OY ": 9_000_000,
    "40 B 888 BB": 999_999_999,
    "40 K 999 BR": 25_000_000,
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
        if m.contact.user_id != m.from_user.id:
            return await m.answer("Faqat o'zingizning kontaktingizni yuboring!")
        phone = m.contact.phone_number
    else:
        return await m.answer("Telefon raqamingizni pastdagi tugma orqali yuboring!")

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
    rasm = MASHINA_RASMLARI.get(d["nomi"])
    if rasm:
        try:
            await m.answer_photo(photo=rasm, caption="Mana sizning mashinangiz:")
        except Exception as e:
            print("Rasm yuborishda xato:", e)


async def main():
    bot = Bot(token="TOKENNI_SHU_YERGA_QOYING")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())