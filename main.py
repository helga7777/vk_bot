from vk_user_info import VkUser
from vk_bot2 import vk_add_button, vk_bot_id_user


if __name__ == '__main__':

    # токен пользователя от приложения
    token = ''

    vk_client = VkUser(token)


    user_id = vk_bot_id_user()

    # если есть данные в бд, то из бд, иначе и записываем в бд

    user_info = vk_client.user(user_id)
    user_search = vk_client.users_search(user_info[0], user_info[1], user_info[2])
    vk_add_button(user_id, user_search)
   
