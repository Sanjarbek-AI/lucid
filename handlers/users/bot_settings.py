from aiogram import types

from filters.private_chat import IsPrivate
from keyboards.default.admins import languages_keyboard, back_admin_main_menu
from keyboards.default.users import back_users_main_menu
from loader import dp, _, bot
from main import config
from utils.db_api.commands import update_language


@dp.message_handler(IsPrivate(), text=["Tilni sozlash ⚙", "Change language ⚙", "Настройка языка ⚙"],
                    chat_id=config.ADMINS)
async def change_language(message: types):
    text = _("Iltimos, o'zingizga qulay tilni tanlang 😊")
    await message.answer(text, reply_markup=await languages_keyboard())


@dp.message_handler(IsPrivate(), text=["O'zbek 🇺🇿"], chat_id=config.ADMINS)
async def change_language(message: types):
    if await update_language("uz", message.chat.id, message):
        text = _("Til o'zgartirildi. ✅", locale="uz")
        await message.answer(text)
    else:
        text = _("Botda muommo mavjud.", locale="uz")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text, reply_markup=await back_admin_main_menu())


@dp.message_handler(IsPrivate(), text=["English 🇺🇸"], chat_id=config.ADMINS)
async def change_language(message: types):
    if await update_language("en", message.chat.id, message):
        text = _("Til o'zgartirildi. ✅", locale="en")
        await message.answer(text)
    else:
        text = _("Botda muommo mavjud.", locale="en")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text, reply_markup=await back_admin_main_menu())


@dp.message_handler(IsPrivate(), text=["Pусский 🇷🇺"], chat_id=config.ADMINS)
async def change_language(message: types):
    if await update_language("ru", message.chat.id, message):
        text = _("Til o'zgartirildi. ✅", locale="ru")
        await message.answer(text)
    else:
        text = _("Botda muommo mavjud.", locale="ru")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text, reply_markup=await back_admin_main_menu())


###############################################################################################################
###############################################################################################################

@dp.message_handler(IsPrivate(), text=["Tilni sozlash ⚙", "Change language ⚙", "Настройка языка ⚙"])
async def change_language(message: types):
    text = _("Iltimos, o'zingizga qulay tilni tanlang 😊")
    await message.answer(text, reply_markup=await languages_keyboard())


@dp.message_handler(IsPrivate(), text=["O'zbek 🇺🇿"])
async def change_language(message: types):
    if await update_language("uz", message.chat.id, message):
        text = _("Til o'zgartirildi. ✅", locale="uz")
        await message.answer(text)
    else:
        text = _("Botda muommo mavjud.", locale="uz")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text, reply_markup=await back_users_main_menu())


@dp.message_handler(IsPrivate(), text=["English 🇺🇸"])
async def change_language(message: types):
    if await update_language("en", message.chat.id, message):
        text = _("Til o'zgartirildi. ✅", locale="en")
        await message.answer(text)
    else:
        text = _("Botda muommo mavjud.", locale="en")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text, reply_markup=await back_users_main_menu())


@dp.message_handler(IsPrivate(), text=["Pусский 🇷🇺"])
async def change_language(message: types):
    if await update_language("ru", message.chat.id, message):
        text = _("Til o'zgartirildi. ✅", locale="ru")
        await message.answer(text)
    else:
        text = _("Botda muommo mavjud.", locale="ru")
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.answer(text, reply_markup=await back_users_main_menu())
