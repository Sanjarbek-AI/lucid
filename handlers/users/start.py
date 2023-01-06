from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import contact_def, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import languages
from keyboards.inline.locations import locations_def
from loader import dp, _
from main import config
from states.users import Register
from utils.db_api.commands import register, get_user_active, register_start, update_user


@dp.message_handler(IsPrivate(), chat_id=config.ADMINS, commands="start")
async def start_admin(message: types.Message, state: FSMContext):
    if await get_user_active(message.from_user.id):
        text = _("Assalomu alaykum. Siz bot boshqaruvchilaridan birisiz. 😊")
        await message.answer(text, reply_markup=await admin_main_menu())
    else:
        await state.update_data({
            "language": "uz",
            "telegram_id": message.chat.id,
            "full_name": message.from_user.full_name,
            "phone_number": "-"
        })

        await register(message, state)
        await state.finish()

        text = _("Assalomu alaykum. Siz bot boshqaruvchilaridan birisiz. 😊")
        await message.answer(text, reply_markup=await admin_main_menu())


@dp.message_handler(IsPrivate(), commands="start")
async def start_users(message: types.Message):
    user = await get_user_active(message.from_user.id)
    if user:
        text = _("Bot xizmatiga xush kelibsiz.")
        await message.answer(text, reply_markup=await users_main_menu())

    else:
        text = "Iltimos, tilni tanlang. 🇺🇿\nВыберите язык. 🇷🇺\nPlease, select language 🇺🇸"
        await Register.language.set()
        await message.answer(text, reply_markup=languages)


@dp.callback_query_handler(state=Register.language)
async def language(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "language": call.data,
    })
    await register_start(call.message, state)

    text = _("Iltimos, Ism va Familiayangizni kiriting.", locale=call.data)
    await Register.full_name.set()
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Register.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await state.update_data({
        "full_name": message.text,
    })
    data = await state.get_data()

    text = _("Iltimos, Telefon raqamingizni kiriting.", locale=data.get('language'))
    await message.answer(text, reply_markup=await contact_def())
    await Register.phone_number.set()


@dp.message_handler(state=Register.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = _("Iltimos tugmadan foydalaning.", locale=data.get('language'))
    await message.answer(text, reply_markup=await contact_def())


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=Register.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data({
        "phone_number": message.contact.phone_number
    })
    data = await state.get_data()

    text = _("Iltimos, doimiy yashash manzilingizni tanlang.", locale=data.get('language'))
    await message.answer(text, reply_markup=await locations_def())
    await Register.location.set()


@dp.callback_query_handler(state=Register.location)
async def location(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "location": call.data,
        "telegram_id": call.from_user.id,
    })
    data = await state.get_data()

    registered_user = await update_user(call.message, state)

    if registered_user:
        text = _("Siz muvofaqqiyatli ro'yxatdan o'tdingiz.", locale=data.get("language"))
    else:
        text = _("Botda nosozlik yuz berdi.", locale=data.get("language"))
    await call.message.answer(text, reply_markup=await users_main_menu())
    await state.finish()
