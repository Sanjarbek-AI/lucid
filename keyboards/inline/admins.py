from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import _
from utils.db_api.commands import get_teachers, get_results

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbek 🇺🇿", callback_data="uz"),
            InlineKeyboardButton(text="Pусский 🇷🇺", callback_data="ru"),
            InlineKeyboardButton(text="English 🇺🇸", callback_data="en")
        ]
    ]
)


async def send_post_def():
    send_post = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Jo'natish ⏫"), callback_data="send_post_yes"),
                InlineKeyboardButton(text=_("Bekor qilish ❌"), callback_data="send_post_no"),
            ]
        ]
    )
    return send_post


async def image_or_file():
    send_post = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Rasm"), callback_data="send_post_image"),
                InlineKeyboardButton(text=_("Video"), callback_data="send_post_file"),
            ],
            [
                InlineKeyboardButton(text=_("Shunchaki matn"), callback_data="nothing")
            ]
        ]
    )
    return send_post


async def text_or_not():
    send_post = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ha"), callback_data="send_post_text_yes"),
                InlineKeyboardButton(text=_("Yo'q"), callback_data="send_post_text_no"),
            ]
        ]
    )
    return send_post



async def link_or_not():
    send_post = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ha"), callback_data="add_link_yes"),
                InlineKeyboardButton(text=_("Yo'q"), callback_data="add_link_no"),
            ]
        ]
    )
    return send_post


callback_comp_ask = CallbackData("comp_yes", "act", "comp_id")


async def new_comp_ask(comp_id):
    comp_ask = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ha"),
                                     callback_data=callback_comp_ask.new(act="comp_yes", comp_id=comp_id)),
                InlineKeyboardButton(text=_("Yo'q"), callback_data="comp_no")
            ]
        ]
    )
    return comp_ask


profile = CallbackData("profile", "act", "lang", "user_id")


async def send_admin_post_all(text, link):
    post_link = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, url=link)
            ]
        ]
    )
    return post_link


async def add_teacher_def():
    add_teacher = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Yangi ustoz ➕"), callback_data="add_teacher"),
            ]
        ]
    )
    return add_teacher


admin_teacher_filter = CallbackData("admin_course", "act", "lang", "teacher_id", "page")
teacher_pagination_next = CallbackData("next_teacher", "act", "lang", "teacher_id", "page")
teacher_pagination_back = CallbackData("back_teacher", "act", "lang", "teacher_id", "page")
teacher_delete = CallbackData("back_course", "act", "lang", "teacher_id", "page")


async def admin_teachers_def(lang, teacher_id, page):
    teachers = await get_teachers()
    both = len(teachers)

    teachers_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_teacher_filter.new(act="admin_teacher", lang="ru",
                                                                            teacher_id=teacher_id, page=page)),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_teacher_filter.new(act="admin_teacher", lang="en",
                                                                            teacher_id=teacher_id, page=page)),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_teacher_filter.new(act="admin_teacher", lang="uz",
                                                                            teacher_id=teacher_id, page=page))
            ],
            [
                InlineKeyboardButton(text=_("Yangi o'qituvchi ➕"), callback_data="add_teacher"),
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=teacher_delete.new(act="delete_teacher", lang="uz",
                                                                      teacher_id=teacher_id, page=page))
            ],
            [
                InlineKeyboardButton(text=_("⬅ Ortga"),
                                     callback_data=teacher_pagination_back.new(act="back_teacher", lang=lang,
                                                                               teacher_id=teacher_id, page=page)),

                InlineKeyboardButton(text=f"{page}/{both}", callback_data="nothing"),

                InlineKeyboardButton(text=_("Keyingi ➡"),
                                     callback_data=teacher_pagination_next.new(act="next_teacher", lang=lang,
                                                                               teacher_id=teacher_id, page=page)),
            ],
        ]
    )
    return teachers_admin


async def add_result_def():
    add_result = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Yangi natija ➕"), callback_data="add_result"),
            ]
        ]
    )
    return add_result


admin_result_filter = CallbackData("admin_result", "act", "lang", "result_id", "page")
result_pagination_next = CallbackData("next_result", "act", "lang", "result_id", "page")
result_pagination_back = CallbackData("back_result", "act", "lang", "result_id", "page")
result_delete = CallbackData("delete_result", "act", "lang", "result_id", "page")


async def admin_results_def(lang, result_id, page):
    results = await get_results()
    both = len(results)

    results_admin = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_result_filter.new(act="admin_result", lang="ru",
                                                                           result_id=result_id, page=page)),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_result_filter.new(act="admin_result", lang="en",
                                                                           result_id=result_id, page=page)),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_result_filter.new(act="admin_result", lang="uz",
                                                                           result_id=result_id, page=page))
            ],
            [
                InlineKeyboardButton(text=_("Yangi natija ➕"), callback_data="add_result"),
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=result_delete.new(act="delete_result", lang="uz",
                                                                     result_id=result_id, page=page))
            ],
            [
                InlineKeyboardButton(text=_("⬅ Ortga"),
                                     callback_data=result_pagination_back.new(act="back_result", lang=lang,
                                                                              result_id=result_id, page=page)),

                InlineKeyboardButton(text=f"{page}/{both}", callback_data="nothing"),

                InlineKeyboardButton(text=_("Keyingi ➡"),
                                     callback_data=result_pagination_next.new(act="next_result", lang=lang,
                                                                              result_id=result_id, page=page)),
            ],
        ]
    )
    return results_admin


admin_contact_filter = CallbackData("admin_contact", "act", "lang")
contact_delete = CallbackData("delete_contact", "act", "lang", "contact_id")


async def contact_admin_def(lang, contact_id):
    add_contact = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=contact_delete.new(act="delete_contact", lang=lang,
                                                                      contact_id=contact_id))
            ],
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_contact_filter.new(act="admin_contact", lang="ru")),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_contact_filter.new(act="admin_contact", lang="en")),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_contact_filter.new(act="admin_contact", lang="uz"))
            ]
        ]
    )
    return add_contact


async def add_contact_def():
    add_contact = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ma'lumot qo'shish ➕"), callback_data="add_contact"),
            ]
        ]
    )
    return add_contact


admin_information_filter = CallbackData("admin_information", "act", "lang")
information_delete = CallbackData("delete_information", "act", "lang", "information_id")


async def information_admin_def(lang, information_id):
    add_information = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=information_delete.new(act="delete_information", lang=lang,
                                                                          information_id=information_id))
            ],
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_information_filter.new(act="admin_information", lang="ru")),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_information_filter.new(act="admin_information", lang="en")),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_information_filter.new(act="admin_information", lang="uz"))
            ]
        ]
    )
    return add_information


async def add_information_def():
    add_information = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ma'lumot qo'shish ➕"), callback_data="add_information"),
            ]
        ]
    )
    return add_information


admin_advantage_filter = CallbackData("admin_advantage", "act", "lang")
advantage_delete = CallbackData("delete_advantage", "act", "lang", "advantage_id")


async def advantage_admin_def(lang, advantage_id):
    add_advantage = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("O'chirish 🗑"),
                                     callback_data=advantage_delete.new(act="delete_information", lang=lang,
                                                                        advantage_id=advantage_id))
            ],
            [
                InlineKeyboardButton(text=_("Ruscha 🇷🇺"),
                                     callback_data=admin_advantage_filter.new(act="admin_advantage", lang="ru")),
                InlineKeyboardButton(text=_("English 🇺🇸"),
                                     callback_data=admin_advantage_filter.new(act="admin_advantage", lang="en")),
                InlineKeyboardButton(text=_("O'zbek 🇺🇿"),
                                     callback_data=admin_advantage_filter.new(act="admin_advantage", lang="uz"))
            ]
        ]
    )
    return add_advantage


async def add_advantage_def():
    add_advantage = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Ma'lumot qo'shish ➕"), callback_data="add_advantage"),
            ]
        ]
    )
    return add_advantage


async def export_excel_users():
    users_excel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Excel olish (ro'yxatdan o'tganlar)"), callback_data="registered_users"),
                InlineKeyboardButton(text=_("Delete user by phone"), callback_data="delete_user_by_phone"),
            ]
        ]
    )
    return users_excel
