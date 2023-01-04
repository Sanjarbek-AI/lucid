from utils.db_api.user_posts import get_user_active_comp_post


async def check_active_comp_post(user_id, comp_id):
    try:
        post = await get_user_active_comp_post(user_id, comp_id)
        print(post)
        if post:
            return post["id"]
        else:
            return False
    except Exception as exc:
        print(exc)
        return False
