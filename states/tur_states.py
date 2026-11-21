from aiogram.fsm.state import State, StatesGroup

class TurState(StatesGroup):
    transport = State()
    transport_darajasi = State()
    qaytish = State()
    manzil = State()
    nomer = State()
