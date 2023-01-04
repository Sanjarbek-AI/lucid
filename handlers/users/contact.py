from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import contact_admin_def, add_contact_def, admin_contact_filter, contact_delete
from loader import dp, _, bot
from main import config
from states.admins import AddContact
from utils.db_api.commands import get_contact, get_user, add_contact, delete_contact


# contact button function for admins
@dp.message_handler(text=['Contact ☎', 'Aloqa ☎', 'Контакты ☎'], chat_id=config.ADMINS)
async def admin_contact(message: types.Message):
    contact = await get_contact()
    user = await get_user(message.from_user.id)
    if contact:
        lang = user['language']
        await message.answer_photo(
            contact[f'image_{lang}'], caption=contact[f'contact_{lang}'],
            reply_markup=await contact_admin_def(lang, contact['id'])
        )
    else:
        text = _("Ma'lumot mavjud emas, qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_contact_def())


@dp.callback_query_handler(text="add_contact", chat_id=config.ADMINS)
async def change_language(call: CallbackQuery):
    text = _("Iltimos, o'zbek tili uchun rasmni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.image_uz.set()


@dp.message_handler(state=AddContact.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Iltimos, rus tili uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.image_ru.set()


@dp.message_handler(state=AddContact.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("Iltimos, ingliz tili uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.image_en.set()


@dp.message_handler(state=AddContact.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.photo[-1].file_id
    })

    text = _("Iltimos, o'zbek tili uchun matnli ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.contact_uz.set()


@dp.message_handler(state=AddContact.contact_uz, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "contact_uz": message.text
    })

    text = _("Iltimos, rus tili uchun matnli ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.contact_ru.set()


@dp.message_handler(state=AddContact.contact_ru, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "contact_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun matnli ma'lumotni kiriting")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddContact.contact_en.set()


@dp.message_handler(state=AddContact.contact_en, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "contact_en": message.text,
    })

    if await add_contact(message, state):
        text = _("Ma'lumot muvofaqqiyatli qo'shildi. ✅")
    else:
        text = _("Ma'lumot qo'shilmadi. Botda muommo mavjud.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(admin_contact_filter.filter(act="admin_contact"), chat_id=config.ADMINS)
async def change_language(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    contact = await get_contact()
    await call.message.answer_photo(
        contact[f'image_{lang}'], caption=contact[f"contact_{lang}"],
        reply_markup=await contact_admin_def(lang, contact['id'])
    )


@dp.callback_query_handler(contact_delete.filter(act="delete_contact"), chat_id=config.ADMINS)
async def delete_contact_function(call: CallbackQuery, callback_data: dict):
    contact_id = callback_data.get("contact_id")

    if await delete_contact(int(contact_id)):
        text = _("Ma'lumot o'chirildi. ✅")
    else:
        text = _("Botda muommo mavjud.")
    await call.message.answer(text, reply_markup=await admin_main_menu())


# #############################################################################
# #############################################################################
# # contact button function for users

@dp.message_handler(text=['Contact ☎', 'Aloqa ☎', 'Контакты ☎'])
async def admin_contact(message: types.Message):
    contact = await get_contact()
    user = await get_user(message.from_user.id)
    if contact:
        lang = user['language']
        await message.answer_photo(
            contact[f'image_{lang}'], caption=contact[f'contact_{lang}'],
            reply_markup=await users_main_menu()
        )
    else:
        text = _("Ma'lumot mavjud emas.")
        await message.answer(text, reply_markup=await users_main_menu())
