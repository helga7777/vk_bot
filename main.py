from vk_user_info import VkUser
from vk_bot2 import vk_add_button, vk_bot_id_user


if __name__ == '__main__':

    # токен пользователя от приложения
    token = ''

    vk_client = VkUser(token)
    # id_client = 552934290

    user_id = vk_bot_id_user()
    # print(user_id)
    # вернул 
    # user_id =  мой ид вк
    user_info = vk_client.user(user_id)
    # print(user_info)
    # вернул (9930, 1, 33)

    user_search = vk_client.users_search(user_info[0], user_info[1], user_info[2])
    # print(user_search)
    # вернул
    # (18691, [94706459, 308402496, 18474779, 73478812, 56158786, 374075967, 340662952])

    vk_add_button(user_id, user_search)
    # print(vk_client.city('Оренбург'))
