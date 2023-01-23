from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.admins import teacher_pagination_back, teacher_pagination_next, result_pagination_back, \
    result_pagination_next
from loader import _
from utils.db_api.commands import get_teachers, get_results


async def user_teachers_def(lang, teacher_id, page):
    teachers = await get_teachers()
    both = len(teachers)

    teachers_user = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("⬅ Ortga"),
                                     callback_data=teacher_pagination_back.new(act="back_course", lang=lang,
                                                                               teacher_id=teacher_id, page=page)),

                InlineKeyboardButton(text=f"{page}/{both}", callback_data="nothing"),

                InlineKeyboardButton(text=_("Keyingi ➡"),
                                     callback_data=teacher_pagination_next.new(act="next_course", lang=lang,
                                                                               teacher_id=teacher_id, page=page)),
            ]
        ]
    )
    return teachers_user


async def user_results_def(lang, result_id, page):
    results = await get_results()
    both = len(results)

    results_user = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("⬅ Ortga"),
                                     callback_data=result_pagination_back.new(act="back_result", lang=lang,
                                                                              result_id=result_id, page=page)),

                InlineKeyboardButton(text=f"{page}/{both}", callback_data="nothing"),

                InlineKeyboardButton(text=_("Keyingi ➡"),
                                     callback_data=result_pagination_next.new(act="next_result", lang=lang,
                                                                              result_id=result_id, page=page)),
            ]
        ]
    )
    return results_user


video_1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Keyingi video ➡"), callback_data="video_1")
        ]
    ]
)
video_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Keyingi video ➡"), callback_data="video_2")
        ]
    ]
)


register_start_video = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ro'yxatdan o'tish 😊 ", callback_data="register_start_video")
        ]
    ]
)
