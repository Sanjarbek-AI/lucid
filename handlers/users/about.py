from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import information_admin_def, add_information_def, admin_information_filter, \
    information_delete
from loader import dp, _, bot
from main import config
from states.admins import AddInformation
from utils.db_api.commands import get_user, get_about, add_about, delete_about


# about button function for admins
@dp.message_handler(text=["Ma'lumot ℹ", "Information ℹ", "Информацияℹ"], chat_id=config.ADMINS)
async def admin_information(message: types.Message):
    about = await get_about()
    user = await get_user(message.from_user.id)
    if about:
        lang = user['language']
        await message.answer_photo(
            about[f'image_{lang}'], caption=about[f'info_{lang}'],
            reply_markup=await information_admin_def(lang, about['id'])
        )
    else:
        text = _("Ma'lumot mavjud emas, qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_information_def())


@dp.callback_query_handler(text="add_information", chat_id=config.ADMINS)
async def change_language(call: CallbackQuery):
    text = _("Iltimos, o'zbek tili uchun rasmni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddInformation.image_uz.set()


@dp.message_handler(state=AddInformation.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Iltimos, rus tili uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddInformation.image_ru.set()


@dp.message_handler(state=AddInformation.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("Iltimos, ingliz tili uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddInformation.image_en.set()


@dp.message_handler(state=AddInformation.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.photo[-1].file_id
    })

    text = _("Iltimos, o'zbek tili uchun matnli ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddInformation.info_uz.set()


@dp.message_handler(state=AddInformation.info_uz, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_uz": message.text
    })

    text = _("Iltimos, rus tili uchun matnli ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddInformation.info_ru.set()


@dp.message_handler(state=AddInformation.info_ru, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun matnli ma'lumotni kiriting")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddInformation.info_en.set()


@dp.message_handler(state=AddInformation.info_en, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_en": message.text,
    })

    if await add_about(message, state):
        text = _("Ma'lumot muvofaqqiyatli qo'shildi. ✅")
    else:
        text = _("Ma'lumot qo'shilmadi. Botda muommo mavjud.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(admin_information_filter.filter(act="admin_information"), chat_id=config.ADMINS)
async def change_language(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    about = await get_about()
    await call.message.answer_photo(
        about[f'image_{lang}'], caption=about[f"info_{lang}"],
        reply_markup=await information_admin_def(lang, about['id'])
    )


@dp.callback_query_handler(information_delete.filter(act="delete_information"), chat_id=config.ADMINS)
async def delete_contact_function(call: CallbackQuery, callback_data: dict):
    information_id = callback_data.get("information_id")

    if await delete_about(int(information_id)):
        text = _("Ma'lumot o'chirildi. ✅")
    else:
        text = _("Botda muommo mavjud.")
    await call.message.answer(text, reply_markup=await admin_main_menu())


# # #############################################################################
# # #############################################################################
# # # contact button function for users

@dp.message_handler(text=["Ma'lumot ℹ", "Information ℹ", "Информация ℹ"])
async def admin_contact(message: types.Message):
    about = await get_about()
    user = await get_user(message.from_user.id)
    if about:
        lang = user['language']
        await message.answer_photo(
            about[f'image_{lang}'], caption=about[f'info_{lang}'],
            reply_markup=await users_main_menu()
        )
    else:
        text = _("Ma'lumot mavjud emas.")
        await message.answer(text, reply_markup=await users_main_menu())
