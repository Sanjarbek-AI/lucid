from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from keyboards.default.admins import admin_main_menu
from loader import dp, _, bot
from states.admins import Language
from utils.db_api.commands import register


@dp.callback_query_handler(state=Language.select)
async def select_language(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "language": call.data,
        "telegram_id": call.from_user.id,
        "full_name": call.message.from_user.full_name,
        "phone_number": "-"
    })

    user = await register(call.message, state)
    text = _("🤖 Asosiy menyuga xush kelibsiz.", locale=call.data)
    await call.message.answer(text, reply_markup=await admin_main_menu())
    await state.finish()

    if not user:
        await state.finish()
        text = f""" @cncele_bot \n Xato paydo bo'di. \n Function: 'select_language' admin"""
        await bot.send_message(chat_id="-1001713472813", text=text)
