from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


async def users_main_menu():
    user_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Kurslar 🎯")),
                KeyboardButton(text=_("O'qituvchilar 👨‍🏫"))
            ],
            [
                KeyboardButton(text=_("Natijalar 🎖")),
                KeyboardButton(text=_("Afzalliklar ⭐"))
            ],
            [
                KeyboardButton(text=_("Aloqa ☎")),
                KeyboardButton(text=_("Ma'lumot ℹ"))
            ],
            [
                KeyboardButton(text=_("Tilni sozlash ⚙")),
            ]
        ], resize_keyboard=True
    )
    return user_menu
