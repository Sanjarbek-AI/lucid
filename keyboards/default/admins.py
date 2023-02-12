from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _
from utils.db_api.commands import get_courses, get_advantages


async def admin_course_def_new(lang):
    courses = await get_courses()

    courses_admin = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if courses:
        for course in courses:
            courses_admin.insert(course[f'button_{lang}'])

    courses_admin.insert(_("Yangi kurs ➕"))
    courses_admin.insert(_("Asosiy menyu ◀"))
    return courses_admin


async def admin_advantage_def_new(lang):
    advantages = await get_advantages()

    advantages_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if advantages:
        for course in advantages:
            advantages_keyboard.insert(course[f'button_{lang}'])

    advantages_keyboard.insert(_("Afzallik qo'shish ➕"))
    advantages_keyboard.insert(_("Asosiy menyu ◀"))
    return advantages_keyboard


async def admin_main_menu():
    admin_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Biz haqimizda ℹ")),
                KeyboardButton(text=_("O'qituvchilar 👨‍🏫"))
            ],
            [
                KeyboardButton(text=_("Kurslar 🎯")),
                KeyboardButton(text=_("Afzalliklar ⭐"))
            ],
            [
                KeyboardButton(text=_("Natijalar 🎖")),
                KeyboardButton(text=_("Aloqa ☎")),
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
