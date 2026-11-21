from aiogram.utils.keyboard import ReplyKeyboardBuilder
transport = [
    "mashina",
    "samalyot",
    "poyezd"
]
transport_darajasi = [
    "ekanom",
    "biznes",
    "premium"
]
qaytish = [
    "qaytaman",
    "qaytmiman"
]
manzil = [
    "andijon",
    "buxoro",
    "farg'ona",
    "jizzax",
    "xorazm",
    "namangan",
    "navoiy",
    "qashqadaryo",
    "samarqand",
    "sirdaryo",
    "surxondaryo",
    "toshkent"
]
def tur_transport():
    b = ReplyKeyboardBuilder()
    for i in transport:
        b.button(text=i)
    b.adjust(3)
    return b.as_markup(resize_keyboard=True)
def tur_transport_darajasi():
    b = ReplyKeyboardBuilder()
    for i in transport_darajasi:
        b.button(text=i)
    b.adjust(3)
    return b.as_markup(resize_keyboard=True)
def tur_qaytish():
    b = ReplyKeyboardBuilder()
    for i in qaytish:
        b.button(text=i)
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)
def tur_manzil():
    b = ReplyKeyboardBuilder()
    for i in manzil:
        b.button(text=i)
    b.adjust(3)
    return b.as_markup(resize_keyboard=True)
def tur_nomer():
    b = ReplyKeyboardBuilder()
    b.button(text="nomer", request_contact=True)
    return b.as_markup(resize_keyboard=True)
