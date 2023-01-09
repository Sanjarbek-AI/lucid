from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


async def admin_main_menu():
    admin_menu = ReplyKeyboardMarkup(
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
                KeyboardButton(text=_("Statistika 📈")),
                KeyboardButton(text=_("Post Jo'natish ⏫"))
            ],
            [
                KeyboardButton(text=_("Tilni sozlash ⚙"))
            ]
        ], resize_keyboard=True
    )
    return admin_menu


async def back_admin_main_menu():
    admin_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Asosiy menyu ◀")),
            ]
        ], resize_keyboard=True
    )
    return admin_menu


async def back_showroom_menu():
    admin_showroom = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Ortga ◀")),
            ]
        ], resize_keyboard=True
    )
    return admin_showroom


async def contact_def():
    contact = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Telefon raqamni jo'natish 📞"), request_contact=True)
            ]
        ], resize_keyboard=True
    )
    return contact


async def languages_keyboard():
    languages = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="O'zbek 🇺🇿"),
                KeyboardButton(text="Pусский 🇷🇺"),
                KeyboardButton(text="English 🇺🇸")
            ]
        ],
        resize_keyboard=True
    )
    return languages
