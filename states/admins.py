from aiogram.dispatcher.filters.state import State, StatesGroup


class Language(StatesGroup):
    select = State()


class DeleteUser(StatesGroup):
    ask = State()
    delete = State()


class AddCompetition(StatesGroup):
    image_uz = State()
    image_ru = State()
    conditions_uz = State()
    conditions_ru = State()
    gifts_uz = State()
    gifts_ru = State()
    gifts_image_uz = State()
    gifts_image_ru = State()


class AddContact(StatesGroup):
    image_uz = State()
    image_ru = State()
    image_en = State()
    contact_uz = State()
    contact_en = State()
    contact_ru = State()


class SendPost(StatesGroup):
    image_or_file = State()
    image = State()
    file = State()
    caption = State()
    text = State()
    text_wait = State()
    link = State()
    link_yes_or_no = State()
    button_text = State()
    waiting = State()


class UpdateContact(StatesGroup):
    image_uz = State()
    image_ru = State()
    contact_uz = State()
    contact_ru = State()


class AddCourse(StatesGroup):
    image_uz = State()
    image_ru = State()
    image_en = State()
    info_uz = State()
    info_en = State()
    info_ru = State()


class AddTeacher(StatesGroup):
    image_uz = State()
    image_ru = State()
    image_en = State()
    info_uz = State()
    info_en = State()
    info_ru = State()


class AddResult(StatesGroup):
    image_uz = State()
    image_ru = State()
    image_en = State()
    info_uz = State()
    info_en = State()
    info_ru = State()


class AddInformation(StatesGroup):
    image_uz = State()
    image_ru = State()
    image_en = State()
    info_uz = State()
    info_en = State()
    info_ru = State()


class AddAdvantage(StatesGroup):
    image_uz = State()
    image_ru = State()
    image_en = State()
    info_uz = State()
    info_en = State()
    info_ru = State()
