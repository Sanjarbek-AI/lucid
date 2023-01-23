from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import InputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from handlers.users.excel_users import export_users_registered_bot
from keyboards.default.admins import admin_main_menu
from keyboards.inline.admins import export_excel_users
from loader import dp, _
from main import config
from states.admins import DeleteUser
from utils.db_api.commands import get_teachers, get_courses, \
    get_results, get_users, delete_user


@dp.callback_query_handler(text="delete_user_by_phone", chat_id=config.ADMINS)
async def delete_user_function(call: CallbackQuery):
    text = _("Iltimos, telefon raqamni kiriting.\nNamuna: +998999999999")
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
    await DeleteUser.delete.set()


@dp.message_handler(state=DeleteUser.delete, chat_id=config.ADMINS)
async def admin_get_courses(message: types, state: FSMContext):
    if await delete_user(message.text):
        text = _("Ma'lumot o'chirildi. ✅")
    else:
        text = _("Botda muommo mavjud.")

    await state.finish()
    await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(IsPrivate(), text=['Statistika 📈', 'Statistics 📈', 'Статистика 📈'], chat_id=config.ADMINS)
async def admin_get_courses(message: types):
    teachers = await get_teachers()
    courses = await get_courses()
    results = await get_results()
    users = await get_users()

    text = f"""
<b>Foydalanuvchilar</b>: {len(users)}

O'qituvchilar: {len(teachers)}
Natijalar: {len(results)}
Kurslar: {len(courses)}
"""
    await message.answer(text, reply_markup=await export_excel_users())


@dp.callback_query_handler(text="registered_users", chat_id=config.ADMINS)
async def export_excel(call: CallbackQuery):
    users = await get_users()
    excel_file = await export_users_registered_bot(users)

    with open("registered_users.xlsx", "wb") as binary_file:
        binary_file.write(excel_file)
    export_file = InputFile(path_or_bytesio="registered_users.xlsx")
    await call.message.reply_document(export_file)
