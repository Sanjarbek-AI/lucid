from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    electric_status_1 = State()
    electric_status_2 = State()
    language = State()
    location = State()
    full_name = State()
    phone_number = State()


class RegisterLike(StatesGroup):
    language = State()
    location = State()
    full_name = State()
    phone_number = State()

class UserSendPost(StatesGroup):
    images = State()
    text = State()
    waiting = State()
