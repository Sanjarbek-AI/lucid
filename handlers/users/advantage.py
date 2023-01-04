from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import advantage_admin_def, admin_advantage_filter, advantage_delete, \
    add_advantage_def
from loader import dp, _, bot
from main import config
from states.admins import AddAdvantage
from utils.db_api.commands import get_user, get_advantage, add_advantage, delete_advantage


@dp.message_handler(text=["Afzalliklar ⭐", "Advantages ⭐", "Преимущества ⭐"], chat_id=config.ADMINS)
async def admin_advantage(message: types.Message):
    advantage = await get_advantage()
    user = await get_user(message.from_user.id)
    if advantage:
        lang = user['language']
        await message.answer_photo(
            advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'],
            reply_markup=await advantage_admin_def(lang, advantage['id'])
        )
    else:
        text = _("Ma'lumot mavjud emas, qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_advantage_def())


@dp.callback_query_handler(text="add_advantage", chat_id=config.ADMINS)
async def change_language(call: CallbackQuery):
    text = _("Iltimos, o'zbek tili uchun rasmni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_uz.set()


@dp.message_handler(state=AddAdvantage.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Iltimos, rus tili uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_ru.set()


@dp.message_handler(state=AddAdvantage.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("Iltimos, ingliz tili uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_en.set()


@dp.message_handler(state=AddAdvantage.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.photo[-1].file_id
    })

    text = _("Iltimos, o'zbek tili uchun matnli ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.info_uz.set()


@dp.message_handler(state=AddAdvantage.info_uz, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_uz": message.text
    })

    text = _("Iltimos, rus tili uchun matnli ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.info_ru.set()


@dp.message_handler(state=AddAdvantage.info_ru, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun matnli ma'lumotni kiriting")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.info_en.set()


@dp.message_handler(state=AddAdvantage.info_en, chat_id=config.ADMINS)
async def advantage_info(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_en": message.text,
    })

    if await add_advantage(message, state):
        text = _("Ma'lumot muvofaqqiyatli qo'shildi. ✅")
    else:
        text = _("Ma'lumot qo'shilmadi. Botda muommo mavjud.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(admin_advantage_filter.filter(act="admin_advantage"), chat_id=config.ADMINS)
async def change_language(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    advantage = await get_advantage()
    await call.message.answer_photo(
        advantage[f'image_{lang}'], caption=advantage[f"info_{lang}"],
        reply_markup=await advantage_admin_def(lang, advantage['id'])
    )


@dp.callback_query_handler(advantage_delete.filter(act="delete_advantage"), chat_id=config.ADMINS)
async def delete_contact_function(call: CallbackQuery, callback_data: dict):
    advantage_id = callback_data.get("advantage_id")

    if await delete_advantage(int(advantage_id)):
        text = _("Ma'lumot o'chirildi. ✅")
    else:
        text = _("Botda muommo mavjud.")
    await call.message.answer(text, reply_markup=await admin_main_menu())


#
# # # #############################################################################
# # # #############################################################################

@dp.message_handler(text=["Afzalliklar ⭐", "Advantages ⭐", "Преимущества ⭐"])
async def user_advantage(message: types.Message):
    about = await get_advantage()
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
