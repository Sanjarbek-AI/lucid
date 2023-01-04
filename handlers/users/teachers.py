from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admins import add_teacher_def, admin_teachers_def, admin_teacher_filter, teacher_delete, \
    teacher_pagination_next, teacher_pagination_back
from keyboards.inline.users import user_teachers_def
from loader import dp, _, bot
from main import config
from states.admins import AddTeacher
from utils.db_api.commands import get_user, get_teachers, add_teacher, get_teacher, delete_teacher


@dp.message_handler(IsPrivate(), text=["O'qituvchilar 👨‍🏫", "Teachers 👨‍🏫", "Учителя 👨‍🏫"], chat_id=config.ADMINS)
async def admin_get_courses(message: types):
    teachers = await get_teachers()
    user = await get_user(message.from_user.id)
    if teachers:
        lang = user['language']
        for teacher in teachers:
            await message.answer_photo(
                teacher[f'image_{lang}'], caption=teacher[f'info_{lang}'],
                reply_markup=await admin_teachers_def(lang, teacher['id'], 1)
            )
            break
    else:
        text = _("Hozirda ustozlar mavjud emas, yangi ustoz qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_teacher_def())


@dp.callback_query_handler(teacher_delete.filter(act="delete_teacher"), chat_id=config.ADMINS)
async def delete_teacher_function(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    teacher_id = callback_data.get("teacher_id")

    if await delete_teacher(int(teacher_id)):
        text = _("Ma'lumot o'chirildi. ✅")
        await call.message.answer(text)
        teachers = await get_teachers()
        if teachers:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            for teacher in teachers:
                await call.message.answer_photo(
                    teacher[f'image_{lang}'], caption=teacher[f'info_{lang}'],
                    reply_markup=await admin_teachers_def(lang, teacher['id'], 1)
                )
                break
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="add_teacher", chat_id=config.ADMINS)
async def admin_add_teacher(call: CallbackQuery):
    text = _("Iltimos, o'zbek tili uchun ustozning rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddTeacher.image_uz.set()


@dp.message_handler(state=AddTeacher.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def course_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Iltimos, rus tili uchun ustozning rasmini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddTeacher.image_ru.set()


@dp.message_handler(state=AddTeacher.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def course_image_ru(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("Iltimos, ingliz tili uchun ustozning rasmini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddTeacher.image_en.set()


@dp.message_handler(state=AddTeacher.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def course_image_en(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.photo[-1].file_id
    })

    text = _("Iltimos, o'zbek tili uchun ustoz haqida ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddTeacher.info_uz.set()


@dp.message_handler(state=AddTeacher.info_uz, chat_id=config.ADMINS)
async def course_text_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_uz": message.text
    })

    text = _("Iltimos, rus tili uchun ustoz haqida ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddTeacher.info_ru.set()


@dp.message_handler(state=AddTeacher.info_ru, chat_id=config.ADMINS)
async def course_text_ru(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun ustoz haqida ma'lumotni kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddTeacher.info_en.set()


@dp.message_handler(state=AddTeacher.info_en, chat_id=config.ADMINS)
async def course_text_en(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_en": message.text,
    })

    if await add_teacher(message, state):
        text = _("Ustoz muvofaqqiyatli qo'shildi. ✅")
    else:
        text = _("Ma'lumot qo'shilmadi. Botda muommo mavjud.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(admin_teacher_filter.filter(act="admin_teacher"), chat_id=config.ADMINS)
async def function(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    teacher_id = int(callback_data.get("teacher_id"))
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    teacher = await get_teacher(teacher_id)

    if teacher:
        await call.message.answer_photo(
            teacher[f'image_{lang}'], caption=teacher[f"info_{lang}"],
            reply_markup=await admin_teachers_def(lang, teacher_id, page)
        )

    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(teacher_pagination_next.filter(act="next_teacher"), chat_id=config.ADMINS)
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    teachers = await get_teachers()

    new_page = page

    if page >= len(teachers) - 1:
        new_page = (page % len(teachers))
    teachers_list = teachers[new_page:new_page + 1]

    if teachers_list:
        teacher = teachers_list[0]
        await call.message.answer_photo(
            teacher[f'image_{lang}'], caption=teacher[f"info_{lang}"],
            reply_markup=await admin_teachers_def(lang, teacher['id'], new_page + 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(teacher_pagination_back.filter(act="back_teacher"), chat_id=config.ADMINS)
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    teachers = await get_teachers()

    new_page = page
    teachers_list = list()
    if page == 1:
        teachers_list = teachers[-1:]
        new_page = len(teachers) + 1
    elif 1 < page <= len(teachers):
        teachers_list = teachers[new_page - 2:new_page - 1]

    if teachers_list:
        course = teachers_list[0]
        await call.message.answer_photo(
            course[f'image_{lang}'], caption=course[f"info_{lang}"],
            reply_markup=await admin_teachers_def(lang, course['id'], new_page - 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


##############################################################################################################
##############################################################################################################


@dp.message_handler(text=["O'qituvchilar 👨‍🏫", "Teachers 👨‍🏫", "Учителя 👨‍🏫"])
async def admin_courses(message: types.Message):
    teachers = await get_teachers()
    user = await get_user(message.from_user.id)
    if teachers:
        lang = user['language']
        for teacher in teachers:
            await message.answer_photo(
                teacher[f'image_{lang}'], caption=teacher[f'info_{lang}'],
                reply_markup=await user_teachers_def(lang, teacher['id'], 1)
            )
            break
    else:
        text = _("Ma'lumot mavjud emas.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(teacher_pagination_next.filter(act="next_course"))
async def next_teacher(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    teachers = await get_teachers()

    new_page = page

    if page >= len(teachers) - 1:
        new_page = (page % len(teachers))
    teachers_list = teachers[new_page:new_page + 1]

    if teachers_list:
        teacher = teachers_list[0]
        await call.message.answer_photo(
            teacher[f'image_{lang}'], caption=teacher[f"info_{lang}"],
            reply_markup=await user_teachers_def(lang, teacher['id'], new_page + 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(teacher_pagination_back.filter(act="back_course"))
async def back_teacher(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    teachers = await get_teachers()

    new_page = page
    teachers_list = list()
    if page == 1:
        teachers_list = teachers[-1:]
        new_page = len(teachers) + 1
    elif 1 < page <= len(teachers):
        teachers_list = teachers[new_page - 2:new_page - 1]

    if teachers_list:
        teacher = teachers_list[0]
        await call.message.answer_photo(
            teacher[f'image_{lang}'], caption=teacher[f"info_{lang}"],
            reply_markup=await user_teachers_def(lang, teacher['id'], new_page - 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await users_main_menu())
