from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from keyboards.default.admins import admin_main_menu
from keyboards.default.users import users_main_menu
from loader import dp, _
from main import config
from filters.private_chat import IsPrivate


@dp.message_handler(IsPrivate(), text=['Asosiy menyu ◀', 'Главное меню ◀'], chat_id=config.ADMINS, state="*")
async def back_admin_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    text = _("Asosiy menyu.")
    await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(IsPrivate(), text=['Asosiy menyu ◀', 'Главное меню ◀'], state="*")
async def back_admin_main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    text = _("Asosiy menyu.")
    await message.answer(text, reply_markup=await users_main_menu())
