import time

import validators
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import ContentType, ContentTypes
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from filters.private_chat import IsPrivate
from keyboards.default.admins import back_admin_main_menu, admin_main_menu
from keyboards.inline.admins import send_post_def, send_admin_post_all, image_or_file, text_or_not
from loader import dp, _, bot
from main import config
from states.admins import SendPost
from utils.db_api.commands import get_users


@dp.message_handler(IsPrivate(), text=["Post Jo'natish ⏫", "Опубликовать Отправить ⏫"], chat_id=config.ADMINS)
async def send_post(message: types.Message):
    text = "Rasm yoki file jo'natasizmi ? "
    # text = _("Post uchun rasmni kiriting.")
    await message.answer(text, reply_markup=await image_or_file())
    await SendPost.image_or_file.set()


@dp.callback_query_handler(state=SendPost.image_or_file, chat_id=config.ADMINS, text="send_post_image")
async def send_post(call: CallbackQuery):
    text = _("Post uchun rasmni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await SendPost.image.set()


@dp.message_handler(state=SendPost.image, chat_id=config.ADMINS, content_types=ContentType.PHOTO)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "image": message.photo[-1].file_id,
        "video": False
    })

    text = _("Post uchun matn kiritasimi ?")
    await message.answer(text, reply_markup=await text_or_not())
    await SendPost.text_wait.set()


@dp.callback_query_handler(state=SendPost.image_or_file, chat_id=config.ADMINS, text="send_post_file")
async def send_post(call: CallbackQuery):
    text = _("Post uchun video kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await SendPost.file.set()


@dp.message_handler(state=SendPost.file, chat_id=config.ADMINS, content_types=ContentTypes.VIDEO)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "video": message.video.file_id,
        "image": False
    })

    text = _("Post uchun matn kiritasimi ?")
    await message.answer(text, reply_markup=await text_or_not())
    await SendPost.text_wait.set()


@dp.callback_query_handler(state=SendPost.image_or_file, chat_id=config.ADMINS, text="nothing")
async def send_post(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "video": False,
        "image": False,
    })
    text = _("Post uchun matn kiritasimi ?")
    await call.message.answer(text, reply_markup=await text_or_not())
    await SendPost.text_wait.set()


@dp.callback_query_handler(state=SendPost.text_wait, chat_id=config.ADMINS, text="send_post_text_yes")
async def send_post(call: CallbackQuery):
    text = _("Post uchun matnni kiriting.")
    await call.message.answer(text, reply_markup=await back_admin_main_menu())
    await SendPost.text.set()


@dp.message_handler(state=SendPost.text, chat_id=config.ADMINS)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "text": message.text
    })
    text = _("Post uchun pastki havolani kiriting.")
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.link.set()


@dp.callback_query_handler(state=SendPost.text_wait, chat_id=config.ADMINS, text="send_post_text_no")
async def send_post(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('image') == False and data.get('video') == False:
        text = _("Post uchun hech narsa kiritilmadi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())
        await state.finish()
    else:
        await state.update_data({
            "text": False
        })
        text = _("Post uchun pastki havolani kiriting.")
        await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
        await SendPost.link.set()


@dp.message_handler(state=SendPost.link, chat_id=config.ADMINS)
async def send_post(message: types.Message, state: FSMContext):
    link = validators.url(message.text)
    if link:
        await state.update_data({
            "link": message.text
        })
        text = _("Post uchun pastki tugmadagi matnni kiriting.")
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        await SendPost.button_text.set()
    else:
        text = _("Havola noto'g'ri kiritildi.")
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
        await SendPost.link.set()


@dp.message_handler(state=SendPost.button_text, chat_id=config.ADMINS)
async def send_post(message: types.Message, state: FSMContext):
    await state.update_data({
        "button_text": message.text
    })
    data = await state.get_data()

    if data.get('image') and data.get("text"):
        await message.answer_photo(data.get("image"), caption=data.get("text"),
                                   reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))
    elif data.get('image') and data.get('text') == False:
        await message.answer_photo(data.get("image"),
                                   reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))
    elif data.get('image') == False and data.get('text'):
        await message.answer(text=data.get('text'),
                             reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))
    elif data.get('video') and data.get("text"):
        await message.answer_video(data.get("video"), caption=data.get("text"),
                                   reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))
    elif data.get('video') == False and data.get('text'):
        await message.answer_video(video=data.get('video'),
                                   reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))
    elif data.get('video') and data.get('text') == False:
        await message.answer(text=data.get('text'),
                             reply_markup=await send_admin_post_all(data.get("button_text"), data.get("link")))

    elif data.get('image') == False and data.get('video') == False and data.get('text') == False:
        await message.answer("Siz hech qanday parametrlarni kiritmadingiz.", reply_markup=await admin_main_menu())

    answer = "Jo'natishni hohlaysizmi ?"
    await message.answer(answer, reply_markup=await send_post_def())
    await SendPost.waiting.set()


@dp.callback_query_handler(state=SendPost.waiting, text="send_post_yes", chat_id=config.ADMINS)
async def send_post_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = await get_users()
    image = data.get('image')
    video = data.get('video')
    text = data.get('text')
    text_new = _("Habar barcha foydalanuvchilarga yuborilmoqda...")
    await call.message.answer(text_new)
    try:
        if image and text and video is False:
            for user in users:
                try:
                    time.sleep(0.2)
                    await bot.send_photo(chat_id=user["telegram_id"], photo=data.get("image"), caption=data.get("text"),
                                         reply_markup=await send_admin_post_all(data.get("button_text"),
                                                                                data.get("link")))
                except Exception as exc:
                    print(exc)
        elif text is False and image and video is False:
            for user in users:
                try:
                    time.sleep(0.2)
                    await bot.send_photo(chat_id=user["telegram_id"], photo=data.get("image"),
                                         reply_markup=await send_admin_post_all(data.get("button_text"),
                                                                                data.get("link")))
                except Exception as exc:
                    print(exc)

        elif text is False and video and image is False:
            for user in users:
                try:
                    time.sleep(0.2)
                    await bot.send_video(chat_id=user["telegram_id"], video=data.get("video"),
                                         reply_markup=await send_admin_post_all(data.get("button_text"),
                                                                                data.get("link")))
                except Exception as exc:
                    print(exc)

        elif video and text and image is False:
            for user in users:
                try:
                    time.sleep(0.2)
                    await bot.send_video(chat_id=user["telegram_id"], video=data.get("video"), caption=data.get("text"),
                                         reply_markup=await send_admin_post_all(data.get("button_text"),
                                                                                data.get("link")))
                except Exception as exc:
                    print(exc)

        elif video is False and image is False and text:
            for user in users:
                try:
                    time.sleep(0.2)
                    await bot.send_message(chat_id=user["telegram_id"], text=data.get("text"),
                                           reply_markup=await send_admin_post_all(data.get("button_text"),
                                                                                  data.get("link")))
                except Exception as exc:
                    print(exc)
        else:
            print("************************")
            pass

        await state.finish()
        text = _("Habar barcha foydalanuvchilarga jo'natildi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())
    except Exception as exc:
        print(exc)
        await state.finish()
        text = _("Botda nosozlik yuz berdi.")
        await call.message.answer(text, reply_markup=await admin_main_menu())


@dp.callback_query_handler(state=SendPost.waiting, text="send_post_no", chat_id=config.ADMINS)
async def send_post_yes(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
    text = _("Habar bekor qilindi.")
    await call.message.answer(text, reply_markup=await admin_main_menu())
