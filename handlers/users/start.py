from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import contact_def, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import languages
from keyboards.inline.locations import locations_def
from keyboards.inline.users import register_start_video, video_1, video_2
from loader import dp, _, bot
from main import config
from states.users import Register
from utils.db_api.commands import register, get_user_active, update_user, register_video_start, update_user_language


# @dp.message_handler(state="*", chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
# async def course_image_en(message: types.Message):
#     await message.answer(message.video.file_id)


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
        await register_video_start(message)


@dp.callback_query_handler(state=Register.language)
async def language(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "language": call.data,
    })

    await update_user_language(call.message, call.data)

    if call.data == "uz":
        file_id = "BAACAgIAAxkBAAIFW2POmGUR0hIFHixPuj2K_TXsdlJCAALPIQAC7tp5SrqPsRNsc4blLQQ"
    elif call.data == "ru":
        file_id = "BAACAgIAAxkBAAIFW2POmGUR0hIFHixPuj2K_TXsdlJCAALPIQAC7tp5SrqPsRNsc4blLQQ"
    else:
        file_id = "BAACAgIAAxkBAAIFW2POmGUR0hIFHixPuj2K_TXsdlJCAALPIQAC7tp5SrqPsRNsc4blLQQ"

    caption = _("Assalomu alaykum, videoni ko'ring va ajoyib ma'lumotlarga ega bo'ling 😃", locale=call.data)

    await Register.video_1.set()
    await bot.send_video(chat_id=call.message.chat.id, video=file_id, caption=caption, reply_markup=video_1)


@dp.callback_query_handler(text="video_1", state=Register.video_1)
async def video_2_func(call: CallbackQuery):
    file_id = "BAACAgIAAxkBAAIFfWPOninQ7t60EPNevizIjIdHTtreAAJCIAACWp55So-ohKuBsBj-LQQ"
    caption = _("Albatta siz uchun foydali bo'ladi. 🤩")
    await Register.video_2.set()
    await bot.send_video(chat_id=call.message.chat.id, video=file_id, caption=caption,
                         reply_markup=video_2)


@dp.callback_query_handler(text="video_2", state=Register.video_2)
async def video_3_func(call: CallbackQuery):
    file_id = "BAACAgIAAxkBAAIFf2POnkQAAQUbkMdLrI7KSpTAL0fw5AACRCAAAlqeeUpWY07lTfO5IS0E"
    caption = _("Video orqali ko'plab foydali ma'lumotlarga ega bo'ling. 😍")
    await Register.register.set()
    await bot.send_video(chat_id=call.message.chat.id, video=file_id, caption=caption,
                         reply_markup=register_start_video)


@dp.callback_query_handler(text="register_start_video", state=Register.register)
async def register_start(call: CallbackQuery):
    text = _("Iltimos, ism va familiyangizni kiriting.")
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
        text = _("Siz muvafaqqiyatli ro'yxatdan o'tdingiz. ✅", locale=data.get("language"))
    else:
        text = _("Botda nosozlik yuz berdi.", locale=data.get("language"))
    await call.message.answer(text, reply_markup=await users_main_menu())
    await state.finish()
