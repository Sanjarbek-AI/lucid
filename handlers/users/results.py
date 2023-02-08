from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from keyboards.default.admins import admin_main_menu, back_admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import add_result_def, admin_results_def, result_delete, admin_result_filter, \
    result_pagination_next, result_pagination_back
from keyboards.inline.users import user_results_def
from loader import dp, _, bot
from main import config
from states.admins import AddResult
from utils.db_api.commands import get_user, get_results, delete_result, add_result, get_result


@dp.message_handler(IsPrivate(), text=["Natijalar 🎖", "Results 🎖", "Результаты 🎖"], chat_id=config.ADMINS)
async def admin_get_results(message: types):
    results = await get_results()
    user = await get_user(message.from_user.id)
    if results:
        lang = user['language']
        for result in results:
            await message.answer_video(
                result[f'image_{lang}'], caption=result[f'info_{lang}'],
                reply_markup=await admin_results_def(lang, result['id'], 1)
            )
            break
    else:
        text = _("Ma'lumot mavjud emas, qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_result_def())


@dp.callback_query_handler(result_delete.filter(act="delete_result"), chat_id=config.ADMINS)
async def delete_result_function(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    result_id = callback_data.get("result_id")

    if await delete_result(int(result_id)):
        text = _("Ma'lumot o'chirildi. ✅")
        await call.message.answer(text)
        results = await get_results()
        if results:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            for result in results:
                await call.message.answer_video(
                    result[f'image_{lang}'], caption=result[f'info_{lang}'],
                    reply_markup=await admin_results_def(lang, result['id'], 1)
                )
                break
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="add_result", chat_id=config.ADMINS)
async def admin_add_result(call: CallbackQuery):
    text = _("Iltimos, o'zbek tili uchun natijaning videosini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddResult.image_uz.set()


@dp.message_handler(state=AddResult.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
async def result_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.video.file_id
    })

    text = _("Iltimos, rus tili uchun natijaning videosini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddResult.image_ru.set()


@dp.message_handler(state=AddResult.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
async def result_image_ru(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.video.file_id
    })

    text = _("Iltimos, ingliz tili uchun natijaning videosini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddResult.image_en.set()


@dp.message_handler(state=AddResult.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.VIDEO)
async def course_image_en(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.video.file_id
    })

    text = _("Iltimos, o'zbek tili uchun natijaning matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddResult.info_uz.set()


@dp.message_handler(state=AddResult.info_uz, chat_id=config.ADMINS)
async def course_text_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_uz": message.text
    })

    text = _("Iltimos, rus tili uchun natijaning matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddResult.info_ru.set()


@dp.message_handler(state=AddResult.info_ru, chat_id=config.ADMINS)
async def course_text_ru(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun natijaning matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddResult.info_en.set()


@dp.message_handler(state=AddResult.info_en, chat_id=config.ADMINS)
async def course_text_en(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_en": message.text,
    })

    if await add_result(message, state):
        text = _("Ma'lumot muvofaqqiyatli qo'shildi. ✅")
    else:
        text = _("Ma'lumot qo'shilmadi. Botda muommo mavjud.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(admin_result_filter.filter(act="admin_result"), chat_id=config.ADMINS)
async def function_result(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    result_id = int(callback_data.get("result_id"))
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    result = await get_result(result_id)

    if result:
        await call.message.answer_video(
            result[f'image_{lang}'], caption=result[f"info_{lang}"],
            reply_markup=await admin_results_def(lang, result_id, page)
        )

    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(result_pagination_next.filter(act="next_result"), chat_id=config.ADMINS)
async def next_result(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    results = await get_results()

    new_page = page

    if page >= len(results) - 1:
        new_page = (page % len(results))
    results_list = results[new_page:new_page + 1]

    if results_list:
        result = results_list[0]
        await call.message.answer_video(
            result[f'image_{lang}'], caption=result[f"info_{lang}"],
            reply_markup=await admin_results_def(lang, result['id'], new_page + 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(result_pagination_back.filter(act="back_result"), chat_id=config.ADMINS)
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    results = await get_results()

    new_page = page
    results_list = list()
    if page == 1:
        results_list = results[-1:]
        new_page = len(results) + 1
    elif 1 < page <= len(results):
        results_list = results[new_page - 2:new_page - 1]

    if results_list:
        result = results_list[0]
        await call.message.answer_video(
            result[f'image_{lang}'], caption=result[f"info_{lang}"],
            reply_markup=await admin_results_def(lang, result['id'], new_page - 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


##############################################################################################################
##############################################################################################################


@dp.message_handler(text=["Natijalar 🎖", "Results 🎖", "Результаты 🎖"])
async def admin_results(message: types.Message):
    results = await get_results()
    user = await get_user(message.from_user.id)
    if results:
        lang = user['language']
        for result in results:
            await message.answer_video(
                result[f'image_{lang}'], caption=result[f'info_{lang}'],
                reply_markup=await user_results_def(lang, result['id'], 1)
            )
            break
    else:
        text = _("Ma'lumot mavjud emas.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(result_pagination_next.filter(act="next_result"))
async def next_result(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    results = await get_results()

    new_page = page

    if page >= len(results) - 1:
        new_page = (page % len(results))
    results_list = results[new_page:new_page + 1]

    if results_list:
        result = results_list[0]
        await call.message.answer_video(
            result[f'image_{lang}'], caption=result[f"info_{lang}"],
            reply_markup=await user_results_def(lang, result['id'], new_page + 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(result_pagination_back.filter(act="back_result"))
async def back_result(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    results = await get_results()

    new_page = page
    results_list = list()
    if page == 1:
        results_list = results[-1:]
        new_page = len(results) + 1
    elif 1 < page <= len(results):
        results_list = results[new_page - 2:new_page - 1]

    if results_list:
        result = results_list[0]
        await call.message.answer_video(
            result[f'image_{lang}'], caption=result[f"info_{lang}"],
            reply_markup=await user_results_def(lang, result['id'], new_page - 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await users_main_menu())
