from vk_user_info import VkUser
from vk_bot2 import vk_add_button, vk_bot_id_user
from vk_bot_base.ORM_CREATE import User


if __name__ == '__main__':
    # токен пользователя от приложения
    token = ''

    vk_client = VkUser(token)
    User_base = User()
    user_id = vk_bot_id_user()
    user_info_base = User_base.get_user(user_id)
    if user_info_base is None:
        user_info = vk_client.user(user_id)
        User_base.add_user(user_id, user_info[0], user_info[1], user_info[2])
        user_search = vk_client.users_search(user_info[0], user_info[1], user_info[2])
        vk_add_button(user_id, user_search)
    user_search = vk_client.users_search(
                                        user_info_base[0],
                                        user_info_base[1],
                                        user_info_base[2]
        )
    vk_add_button(user_id, user_search)