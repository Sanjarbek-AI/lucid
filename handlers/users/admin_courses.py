from aiogram import types
from aiogram.types import InputFile
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from filters.private_chat import IsPrivate
from handlers.users.excel_users import export_users_registered
from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.default.users import users_main_menu
from keyboards.inline.admin_course import admin_course_def, add_course_def, admin_course_filter, course_delete, \
    course_pagination_next, course_pagination_back, users_course_def, admin_registered_to_course, course_enrolling
from loader import dp, _, bot
from main import config
from states.admins import AddCourse
from utils.db_api.commands import get_user, get_courses, add_course, get_course, delete_course, register_to_course, \
    check_user_register, get_registered_users


@dp.message_handler(IsPrivate(), text=['Kurslar 🎯', 'Courses 🎯', "Курсы 🎯"], chat_id=config.ADMINS)
async def admin_get_courses(message: types):
    courses = await get_courses()
    user = await get_user(message.from_user.id)
    if courses:
        lang = user['language']
        for course in courses:
            await message.answer_photo(
                course[f'image_{lang}'], caption=course[f'info_{lang}'],
                reply_markup=await admin_course_def(lang, course['id'], 1)
            )
            break
    else:
        text = _("Hozirda kurslar mavjud emas, yangi kurs qo'shish uchun pastdagi tugmadan foydalaning.")
        await message.answer(text, reply_markup=await add_course_def())


@dp.callback_query_handler(course_delete.filter(act="delete_course"), chat_id=config.ADMINS)
async def delete_courses(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    course_id = callback_data.get("course_id")

    if await delete_course(int(course_id)):
        text = _("Kurs o'chirildi. ✅")
        await call.message.answer(text)
        courses = await get_courses()
        if courses:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            for course in courses:
                await call.message.answer_photo(
                    course[f'image_{lang}'], caption=course[f'info_{lang}'],
                    reply_markup=await admin_course_def(lang, course['id'], 1)
                )
                break
    else:
        text = _("Did not added. Bot has some problem.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(text="add_course", chat_id=config.ADMINS)
async def admin_add_course(call: CallbackQuery):
    text = _("Iltimos, o'zbek tili uchun kurs rasmini kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCourse.image_uz.set()


@dp.message_handler(state=AddCourse.image_uz, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def course_image_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_uz": message.photo[-1].file_id
    })

    text = _("Iltimos, rus tili uchun kurs rasmini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCourse.image_ru.set()


@dp.message_handler(state=AddCourse.image_ru, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def course_image_ru(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_ru": message.photo[-1].file_id
    })

    text = _("Iltimos, ingliz tili uchun kurs rasmini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCourse.image_en.set()


@dp.message_handler(state=AddCourse.image_en, chat_id=config.ADMINS, content_types=types.ContentTypes.PHOTO)
async def course_image_en(message: types.Message, state: FSMContext):
    await state.update_data({
        "image_en": message.photo[-1].file_id
    })

    text = _("Iltimos, o'zbek tili uchun kurs matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCourse.info_uz.set()


@dp.message_handler(state=AddCourse.info_uz, chat_id=config.ADMINS)
async def course_text_uz(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_uz": message.text
    })

    text = _("Iltimos, rus tili uchun kurs matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCourse.info_ru.set()


@dp.message_handler(state=AddCourse.info_ru, chat_id=config.ADMINS)
async def course_text_ru(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_ru": message.text
    })

    text = _("Iltimos, ingliz tili uchun kurs matnini kiriting.")
    await message.answer(text, reply_markup=await back_admin_main_menu())
    await AddCourse.info_en.set()


@dp.message_handler(state=AddCourse.info_en, chat_id=config.ADMINS)
async def course_text_en(message: types.Message, state: FSMContext):
    await state.update_data({
        "info_en": message.text,
    })

    if await add_course(message, state):
        text = _("Kurs muvofaqqiyatli qo'shildi. ✅")
    else:
        text = _("Kurs qo'shilmadi. Botda qandaydir muommo mavjud.")
    await message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()


@dp.callback_query_handler(admin_course_filter.filter(act="admin_course"), chat_id=config.ADMINS)
async def change_language(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    course_id = int(callback_data.get("course_id"))
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    course = await get_course(course_id)

    if course:
        await call.message.answer_photo(
            course[f'image_{lang}'], caption=course[f"info_{lang}"],
            reply_markup=await admin_course_def(lang, course_id, page)
        )

    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(course_pagination_next.filter(act="next_course"), chat_id=config.ADMINS)
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    course_id = callback_data.get("course_id")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    courses = await get_courses()

    new_page = page

    if page >= len(courses) - 1:
        new_page = (page % len(courses))
    course_list = courses[new_page:new_page + 1]

    if course_list:
        course = course_list[0]
        await call.message.answer_photo(
            course[f'image_{lang}'], caption=course[f"info_{lang}"],
            reply_markup=await admin_course_def(lang, course['id'], new_page + 1)
        )
    else:
        text = _("Bot has some problems.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(course_pagination_back.filter(act="back_course"), chat_id=config.ADMINS)
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    course_id = callback_data.get("course_id")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    courses = await get_courses()

    new_page = page
    course_list = list()
    if page == 1:
        course_list = courses[-1:]
        new_page = len(courses) + 1
    elif 1 < page <= len(courses):
        course_list = courses[new_page - 2:new_page - 1]

    if course_list:
        course = course_list[0]
        await call.message.answer_photo(
            course[f'image_{lang}'], caption=course[f"info_{lang}"],
            reply_markup=await admin_course_def(lang, course['id'], new_page - 1)
        )
    else:
        text = _("Bot has some problems.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(admin_registered_to_course.filter(act="registered_to_course"), chat_id=config.ADMINS)
async def user_register_to_course(call: CallbackQuery, callback_data: dict, state: FSMContext):
    course_id = callback_data.get("course_id")
    users_list = await get_registered_users(int(course_id))
    if users_list:
        users_id_list = [user["user_id"] for user in users_list]
        users = list()
        for user in users_id_list:
            user_data = await get_user(user)
            users.append(user_data)
        excel_file = await export_users_registered(users, course_id)
        with open("users.xlsx", "wb") as binary_file:
            binary_file.write(excel_file)
        export_file = InputFile(path_or_bytesio="users.xlsx")
        await call.message.reply_document(export_file)


##############################################################################################################
##############################################################################################################


@dp.message_handler(text=['Courses 🎯', "Kurslar 🎯", 'Курсы 🎯'])
async def admin_courses(message: types.Message):
    courses = await get_courses()
    user = await get_user(message.from_user.id)
    if courses:
        lang = user['language']
        for course in courses:
            await message.answer_photo(
                course[f'image_{lang}'], caption=course[f'info_{lang}'],
                reply_markup=await users_course_def(lang, course['id'], 1)
            )
            break
    else:
        text = _("Hozirda faol kurslar mavjud emas.")
        await message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(course_pagination_next.filter(act="next_course"))
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    courses = await get_courses()

    new_page = page

    if page >= len(courses) - 1:
        new_page = (page % len(courses))
    course_list = courses[new_page:new_page + 1]

    if course_list:
        course = course_list[0]
        await call.message.answer_photo(
            course[f'image_{lang}'], caption=course[f"info_{lang}"],
            reply_markup=await users_course_def(lang, course['id'], new_page + 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(course_pagination_back.filter(act="back_course"))
async def next_course(call: CallbackQuery, callback_data: dict):
    lang = callback_data.get("lang")
    page = int(callback_data.get("page"))

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    courses = await get_courses()

    new_page = page
    course_list = list()
    if page == 1:
        course_list = courses[-1:]
        new_page = len(courses) + 1
    elif 1 < page <= len(courses):
        course_list = courses[new_page - 2:new_page - 1]

    if course_list:
        course = course_list[0]
        await call.message.answer_photo(
            course[f'image_{lang}'], caption=course[f"info_{lang}"],
            reply_markup=await users_course_def(lang, course['id'], new_page - 1)
        )
    else:
        text = _("Botda muommo mavjud.")
        await call.message.answer(text, reply_markup=await users_main_menu())


@dp.callback_query_handler(course_enrolling.filter(act="register_to_course"))
async def user_register_to_course(call: CallbackQuery, callback_data: dict, state: FSMContext):
    course_id = callback_data.get("course_id")

    if await check_user_register(int(course_id), int(call.message.chat.id)):
        text = _("Siz bu kursga ro'yxatdan o'tgansiz. ✅")
        await call.message.answer(text, reply_markup=await users_main_menu())
    else:
        await state.update_data({
            "course_id": int(course_id),
            "user_id": int(call.message.chat.id),
        })

        if await register_to_course(call.message, state):
            text = _("Siz muvofaqqiyatli ro'yxatdan o'tdingiz. ✅\nTez orada siz bilan bog'lanamiz. 😊")
        else:
            text = _("Botda muommo mavjud.")

        await state.finish()
        await call.message.answer(text, reply_markup=await users_main_menu())
