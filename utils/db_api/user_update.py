from main.databases import database
from main.models import *


async def update_user_full_name(message, full_name, user_id):
    try:
        query = users.update().values(
            full_name=full_name,
            updated_at=message.date
        ).where(users.c.telegram_id == user_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_user_phone_number(message, phone_number, user_id):
    try:
        query = users.update().values(
            phone_number=phone_number,
            updated_at=message.date
        ).where(users.c.telegram_id == user_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_user_location(message, location, user_id):
    try:
        query = users.update().values(
            location=location,
            updated_at=message.date
        ).where(users.c.telegram_id == user_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_user_language(message, language, user_id):
    try:
        query = users.update().values(
            language=language,
            updated_at=message.date
        ).where(users.c.telegram_id == user_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False
