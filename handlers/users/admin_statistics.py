from aiogram import types
from aiogram.types import InputFile
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from handlers.users.excel_users import export_users_registered_bot
from keyboards.inline.admins import export_excel_users
from loader import dp
from main import config
from utils.db_api.commands import get_teachers, get_courses, \
    get_results, get_users


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
