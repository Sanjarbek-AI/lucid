from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from keyboards.default.admins import back_admin_main_menu, admin_main_menu, admin_advantage_def_new
from keyboards.default.users import users_main_menu, user_advantage_def_new
from keyboards.inline.admins import admin_advantage_filter, advantage_delete, advantage_admin_def
from loader import dp, _, bot
from main import config
from states.admins import AddAdvantage, Menu
from utils.db_api.commands import get_user, add_advantage, delete_advantage, get_advantages, get_advantage_by_button, \
    get_advantage


@dp.message_handler(text=["Afzalliklar ⭐", "Advantages ⭐", "Преимущества ⭐"], chat_id=config.ADMINS)
async def admin_advantage(message: types.Message):
    await Menu.advantage.set()
    advantages = await get_advantages()
    user = await get_user(message.from_user.id)
    lang = user['language']
    if advantages:
        text = _("Afzalliklar menyusi, kerakli tugmani tanlang.")
    else:
        text = _("Ma'lumot mavjud emas, qo'shish uchun pastdagi tugmadan foydalaning.")
    await message.answer(text, reply_markup=await admin_advantage_def_new(lang))


@dp.message_handler(text=["Afzallik qo'shish ➕", "Добавить предпочтение ➕", "Add advantage ➕"], chat_id=config.ADMINS,
                    state=Menu.advantage)
async def add_advantage_handler(message: types.Message):
    text = _("Iltimos, o'zbek tili uchun afzallik nomini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.button_uz.set()


@dp.message_handler(state=AddAdvantage.button_uz, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "button_uz": message.text
    })

    text = _("Iltimos, rus tili uchun afzallik nomini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.button_ru.set()


@dp.message_handler(state=AddAdvantage.button_ru, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "button_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun afzallik nomini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.button_en.set()


@dp.message_handler(state=AddAdvantage.button_en, chat_id=config.ADMINS)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "button_en": message.text
    })

    text = _("Iltimos, o'zbek tili uchun rasm yoki video kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_uz.set()


@dp.message_handler(state=AddAdvantage.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Iltimos, rus tili uchun rasm yoki video kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_ru.set()


@dp.message_handler(state=AddAdvantage.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.video.file_id
    })

    text = _("Iltimos, rus tili uchun rasm yoki video kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_ru.set()


@dp.message_handler(state=AddAdvantage.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("Iltimos, ingliz tili uchun rasm yoki video kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddAdvantage.image_en.set()


@dp.message_handler(state=AddAdvantage.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.video.file_id
    })

    text = _("Iltimos, ingliz tili uchun rasm yoki video kiriting.")
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


@dp.message_handler(state=AddAdvantage.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
async def contact_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.video.file_id
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


@dp.callback_query_handler(admin_advantage_filter.filter(act="admin_advantage"), chat_id=config.ADMINS,
                           state=Menu.advantage)
async def change_language(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    advantage_id = callback_data.get("advantage_id")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    advantage = await get_advantage(advantage_id)
    try:
        await call.message.answer_video(advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'],
                                        reply_markup=await advantage_admin_def(lang, advantage['id']))
    except:
        await call.message.answer_photo(advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'],
                                        reply_markup=await advantage_admin_def(lang, advantage['id']))


@dp.callback_query_handler(advantage_delete.filter(act="delete_advantage"), chat_id=config.ADMINS, state=Menu.advantage)
async def delete_function(call: CallbackQuery, callback_data: dict):
    try:
        user = await get_user(call.message.chat.id)
        lang = user['language']
        advantage_id = callback_data.get("advantage_id")

        if await delete_advantage(int(advantage_id)):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            text = _("Kurs o'chirildi. ✅\nKurslar menyusi, kerakli kursni tanlang.")
            await call.message.answer(text=text, reply_markup=await admin_advantage_def_new(lang))
        else:
            text = _("Botda muommo mavjud.")
            await call.message.answer(text, reply_markup=await admin_main_menu())
    except Exception as exc:
        print(exc)


@dp.message_handler(IsPrivate(), chat_id=config.ADMINS, state=Menu.advantage)
async def admin_get_advantages(message: types.Message):
    user = await get_user(message.from_user.id)
    lang = user['language']
    advantage = await get_advantage_by_button(message.text)

    if advantage:
        try:
            await message.answer_video(advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'],
                                       reply_markup=await advantage_admin_def(lang, advantage['id']))
        except:
            await message.answer_photo(advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'],
                                       reply_markup=await advantage_admin_def(lang, advantage['id']))
    else:
        text = _("Bunday nomdagi afzallik mavjud emas !")
        await message.answer(text, reply_markup=await admin_advantage_def_new(lang))


# # # #############################################################################
# # # #############################################################################

@dp.message_handler(text=["Afzalliklar ⭐", "Advantages ⭐", "Преимущества ⭐"])
async def user_advantage(message: types.Message):
    await Menu.advantage.set()
    advantages = await get_advantages()
    user = await get_user(message.from_user.id)
    lang = user['language']

    if advantages:
        text = _("Afzalliklar menyusi, bizning ustun taraflarimiz bilan tanishing.")
        await message.answer(text, reply_markup=await user_advantage_def_new(lang))
    else:
        text = _("Ma'lumot mavjud emas.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.message_handler(IsPrivate(), state=Menu.advantage)
async def admin_get_advantages(message: types.Message):
    user = await get_user(message.from_user.id)
    lang = user['language']
    advantage = await get_advantage_by_button(message.text)

    if advantage:
        try:
            await message.answer_video(advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'])
        except:
            await message.answer_photo(advantage[f'image_{lang}'], caption=advantage[f'info_{lang}'])
    else:
        text = _("Bunday nomdagi afzallik mavjud emas !")
        await message.answer(text, reply_markup=await user_advantage_def_new(lang))
