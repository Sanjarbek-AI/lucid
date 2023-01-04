from aiogram import executor

from loader import dp, bot
import middlewares, filters, handlers
from main.databases import database
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await database.connect()
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    await database.disconnect()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
