from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _

admin_course_filter = CallbackData("admin_course", "act", "lang", "course_id")
registered_to_course_callback = CallbackData("registered_to_course", "act", "course_id")
course_delete = CallbackData("back_course", "act", "lang", "course_id")


async def admin_course_def(lang, course_id):
    courses_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_course_filter.new(act="admin_course", lang="ru",
                                                                           course_id=course_id)),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_course_filter.new(act="admin_course", lang="en",
                                                                           course_id=course_id)),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_course_filter.new(act="admin_course", lang="uz",
                                                                           course_id=course_id))
            ],
            [
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=course_delete.new(act="delete_course", lang="uz",
                                                                     course_id=course_id))
            ],
            [
                InlineKeyboardButton(text=_("Ro'yxatdan o'tganlar"),
                                     callback_data=registered_to_course_callback.new(act="registered_to_course",
                                                                                     course_id=course_id))
            ]
        ]
    )
    return courses_admin


course_enrolling = CallbackData("register_to_course", "act", "course_id")


async def register_course(course_id):
    courses_user = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(text=_("Ro'yxatdan o'tish ➕"),
                                     callback_data=course_enrolling.new(act="register_to_course", course_id=course_id))
            ]
        ]
    )
    return courses_user
