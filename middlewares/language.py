from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from main.config import I18N_DOMAIN, LOCALES_DIR
from utils.db_api.commands import get_user


async def get_lang(user_id):
    user = await get_user(user_id)
    if user:
        return user["language"]
    else:
        return "uz"


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action, args):
        user = types.User.get_current()
        return await get_lang(user.id)


def setup_middleware(dp_):
    i18n_ = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp_.middleware.setup(i18n_)
    return i18n_
