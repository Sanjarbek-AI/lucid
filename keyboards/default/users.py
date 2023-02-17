from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _
from utils.db_api.commands import get_courses, get_advantages


async def users_main_menu():
    user_menu = ReplyKeyboardMarkup(
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
                KeyboardButton(text=_("Tilni sozlash ⚙")),
            ]
        ], resize_keyboard=True
    )
    return user_menu


async def back_users_main_menu():
    user_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Asosiy menyu ◀")),
            ]
        ], resize_keyboard=True
    )
    return user_menu


async def user_course_def_new(lang):
    courses = await get_courses()

    courses_admin = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if courses:
        for course in courses:
            courses_admin.insert(course[f'button_{lang}'])

    courses_admin.insert(_("Asosiy menyu ◀"))
    return courses_admin


async def user_advantage_def_new(lang):
    advantages = await get_advantages()

    advantage_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if advantages:
        for advantage in advantages:
            advantage_keyboard.insert(advantage[f'button_{lang}'])

    advantage_keyboard.insert(_("Asosiy menyu ◀"))
    return advantage_keyboard
