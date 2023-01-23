from aiogram.dispatcher.filters.state import StatesGroup, State


class Video(StatesGroup):
    video_1 = State()


class Register(StatesGroup):
    video_1 = State()
    video_2 = State()
    register = State()
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
