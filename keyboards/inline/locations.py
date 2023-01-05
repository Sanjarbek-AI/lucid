from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

from loader import _


async def locations_def():
    locations = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("Andijon"), callback_data="Andijon"),
                InlineKeyboardButton(text=_("Buxoro"), callback_data="Buxoro")
            ],
            [
                InlineKeyboardButton(text=_("Farg'ona"), callback_data="Farg'ona"),
                InlineKeyboardButton(text=_("Jizzax"), callback_data="Jizzax")
            ],
            [
                InlineKeyboardButton(text=_("Xorazm"), callback_data="Xorazm"),
                InlineKeyboardButton(text=_("Namangan"), callback_data="Namangan")
            ],
            [
                InlineKeyboardButton(text=_("Navoiy"), callback_data="Navoiy"),
                InlineKeyboardButton(text=_("Qashqadaryo"), callback_data="Qashqadaryo")
            ],
            [
                InlineKeyboardButton(text=_("Samanrqand"), callback_data="Samarqand"),
                InlineKeyboardButton(text=_("Sirdaryo"), callback_data="Sirdaryo")
            ],
            [
                InlineKeyboardButton(text=_("Surxondaryo"), callback_data="Surxondaryo"),
                InlineKeyboardButton(text=_("Toshkent V"), callback_data="Toshkent_viloyati")
            ],
            [
                InlineKeyboardButton(text=_("Toshkent shahri"), callback_data="Toshkent_shahri"),
            ],
            [
                InlineKeyboardButton(text=_("Qoraqalpog'iston Respublikasi"),
                                     callback_data="Qoraqalpog'iston_Respublikasi"),
            ]
        ]
    )
    return locations


languages_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbek 🇺🇿", callback_data="uz"),
            InlineKeyboardButton(text="Pусский 🇷🇺", callback_data="ru"),
            InlineKeyboardButton(text="English 🇺🇸", callback_data="en"),
        ]
    ]
)
