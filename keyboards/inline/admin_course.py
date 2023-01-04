from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import _
from utils.db_api.commands import get_courses

admin_course_filter = CallbackData("admin_course", "act", "lang", "course_id", "page")
admin_registered_to_course = CallbackData("registered_to_course", "act", "lang", "course_id", "page")
course_pagination_next = CallbackData("next_course", "act", "lang", "course_id", "page")
course_pagination_back = CallbackData("back_course", "act", "lang", "course_id", "page")
course_delete = CallbackData("back_course", "act", "lang", "course_id", "page")


async def admin_course_def(lang, course_id, page):
    courses = await get_courses()
    both = len(courses)

    courses_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_course_filter.new(act="admin_course", lang="ru",
                                                                           course_id=course_id, page=page)),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_course_filter.new(act="admin_course", lang="en",
                                                                           course_id=course_id, page=page)),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_course_filter.new(act="admin_course", lang="uz",
                                                                           course_id=course_id, page=page))
            ],
            [
                InlineKeyboardButton(text=_("Yangu kurs ➕"), callback_data="add_course"),
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=course_delete.new(act="delete_course", lang="uz",
                                                                     course_id=course_id, page=page))
            ],
            [
                InlineKeyboardButton(text=_("Ro'yxatdan o'tganlar 👤"),
                                     callback_data=admin_registered_to_course.new(act="registered_to_course", lang=lang,
                                                                                  course_id=course_id, page=page)),
            ],
            [
                InlineKeyboardButton(text=_("⬅ Ortga"),
                                     callback_data=course_pagination_back.new(act="back_course", lang=lang,
                                                                              course_id=course_id, page=page)),

                InlineKeyboardButton(text=f"{page}/{both}", callback_data="nothing"),

                InlineKeyboardButton(text=_("Keyingi ➡"),
                                     callback_data=course_pagination_next.new(act="next_course", lang=lang,
                                                                              course_id=course_id, page=page)),
            ],
        ]
    )
    return courses_admin


async def add_course_def():
    add_course = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Yangi kurs ➕"), callback_data="add_course"),
            ]
        ]
    )
    return add_course


course_enrolling = CallbackData("register_to_course", "act", "lang", "course_id", "page")


async def users_course_def(lang, course_id, page):
    courses = await get_courses()
    both = len(courses)

    courses_user = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("⬅ Ortga"),
                                     callback_data=course_pagination_back.new(act="back_course", lang=lang,
                                                                              course_id=course_id, page=page)),

                InlineKeyboardButton(text=f"{page}/{both}", callback_data="nothing"),

                InlineKeyboardButton(text=_("Keyingi ➡"),
                                     callback_data=course_pagination_next.new(act="next_course", lang=lang,
                                                                              course_id=course_id, page=page)),
            ],
            [
                InlineKeyboardButton(text=_("Ro'yxatdan o'tish ➕"),
                                     callback_data=course_enrolling.new(act="register_to_course", lang=lang,
                                                                        course_id=course_id, page=page))
            ]
        ]
    )
    return courses_user
