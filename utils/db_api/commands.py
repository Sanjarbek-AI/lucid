from main.databases import database
from main.models import *


async def get_user(telegram_id):
    try:
        query = users.select().where(users.c.telegram_id == telegram_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users_in_list(users_list):
    try:
        query = users.select().where(users.c.telegram_id in users_list)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_user_active(telegram_id):
    try:
        query = users.select().where(users.c.telegram_id == telegram_id, users.c.status == UserStatus.active)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users_list(id_list):
    try:
        query = users.select().where(users.c.telegram_id in id_list)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users():
    try:
        query = users.select().where(users.c.status == UserStatus.active)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_electric_users():
    try:
        query = users.select().where(users.c.electric_status == 1)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_users_status_false():
    try:
        query = users.select().where(users.c.status == UserStatus.inactive)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def register(message, state):
    try:
        data = await state.get_data()
        query = users.insert().values(
            telegram_id=data.get("telegram_id"),
            full_name=data.get("full_name"),
            location=data.get("location"),
            language=data.get("language"),
            phone_number=data.get("phone_number"),
            status=UserStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_user_status(message, state):
    try:
        data = await state.get_data()
        query = users.update().values(
            telegram_id=data.get("telegram_id"),
            full_name=data.get("full_name"),
            location=data.get("location"),
            language=data.get("language"),
            phone_number=data.get("phone_number"),
            status=UserStatus.active,
            updated_at=message.date
        ).where(users.c.telegram_id == data.get("telegram_id"))
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def register_start(message, lang):
    try:
        query = users.insert().values(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            language=lang,
            status=UserStatus.inactive,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_courses():
    try:
        query = courses.select().where(courses.c.status == CourseStatus.active)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_course(course_id):
    try:
        query = courses.select().where(courses.c.status == CourseStatus.active, courses.c.id == course_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_course(course_id):
    try:
        query = courses.delete().where(courses.c.id == course_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def register_to_course(message, state):
    try:
        data = await state.get_data()
        query = registered_to_course.insert().values(
            course_id=data.get("course_id"),
            user_id=data.get("user_id"),
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def check_user_register(course_id, user_id):
    try:
        query = registered_to_course.select().where(registered_to_course.c.course_id == course_id,
                                                    registered_to_course.c.user_id == user_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_registered_users(course_id):
    try:
        query = registered_to_course.select().where(registered_to_course.c.course_id == course_id)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def add_course(message, state):
    try:
        data = await state.get_data()
        query = courses.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            image_en=data.get("image_en"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            info_en=data.get("info_en"),
            status=CourseStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_teachers():
    try:
        query = teachers.select().where(teachers.c.status == TeacherStatus.active)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_teacher(teacher_id):
    try:
        query = teachers.select().where(teachers.c.status == TeacherStatus.active,
                                        teachers.c.id == teacher_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_teacher(teacher_id):
    try:
        query = teachers.delete().where(teachers.c.id == teacher_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_teacher(message, state):
    try:
        data = await state.get_data()
        query = teachers.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            image_en=data.get("image_en"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            info_en=data.get("info_en"),
            status=TeacherStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_results():
    try:
        query = results.select().where(results.c.status == ResultStatus.active)
        return await database.fetch_all(query=query)
    except Exception as exc:
        print(exc)
        return False


async def get_result(result_id):
    try:
        query = results.select().where(results.c.status == ResultStatus.active,
                                       results.c.id == result_id)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_result(result_id):
    try:
        query = results.delete().where(results.c.id == result_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_result(message, state):
    try:
        data = await state.get_data()
        query = results.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            image_en=data.get("image_en"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            info_en=data.get("info_en"),
            status=ResultStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def delete_contact(contact_id):
    try:
        query = contacts.delete().where(contacts.c.id == contact_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_contact():
    try:
        query = contacts.select().where(contacts.c.status == ContactStatus.active)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def add_contact(message, state):
    try:
        data = await state.get_data()
        query = contacts.insert().values(
            image_uz=data.get("image_uz"),
            image_en=data.get("image_en"),
            image_ru=data.get("image_ru"),
            contact_uz=data.get("contact_uz"),
            contact_en=data.get("contact_en"),
            contact_ru=data.get("contact_ru"),
            status=ContactStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_about():
    try:
        query = about.select().where(about.c.status == AboutStatus.active)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_about(about_id):
    try:
        query = about.delete().where(about.c.id == about_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_about(message, state):
    try:
        data = await state.get_data()
        query = about.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            image_en=data.get("image_en"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            info_en=data.get("info_en"),
            status=AboutStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def get_advantage():
    try:
        query = advantage.select().where(advantage.c.status == AdvantageStatus.active)
        return await database.fetch_one(query=query)
    except Exception as exc:
        print(exc)
        return False


async def delete_advantage(advantage_id):
    try:
        query = advantage.delete().where(advantage.c.id == advantage_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def add_advantage(message, state):
    try:
        data = await state.get_data()
        query = advantage.insert().values(
            image_uz=data.get("image_uz"),
            image_ru=data.get("image_ru"),
            image_en=data.get("image_en"),
            info_uz=data.get("info_uz"),
            info_ru=data.get("info_ru"),
            info_en=data.get("info_en"),
            status=AdvantageStatus.active,
            created_at=message.date,
            updated_at=message.date
        )
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False


async def update_language(new_lang, telegram_id, message):
    try:
        query = users.update().values(
            language=new_lang,
            updated_at=message.date
        ).where(users.c.status == UserStatus.active, users.c.telegram_id == telegram_id)
        await database.execute(query=query)
        return True
    except Exception as exc:
        print(exc)
        return False
