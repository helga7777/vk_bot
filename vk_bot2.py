from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
import vk_api
import requests
from io import BytesIO
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_user_info import VkUser
from vk_button import vk_add_button



token = ''
vk = vk_api.VkApi(token=token)
vk._auth_token()
longpoll = VkLongPoll(vk)

# токен пользователя от приложения
token1 = ''
vk_client = VkUser(token1)


def vk_bot_id_user():
    value = {
            'offset': 0,
            'count': 20,
            'filter': 'unanswered'
    }

    messages = vk.method('messages.getConversations', value)
    if messages['count'] >= 1:
        user_id = messages['items'][0]['last_message']['from_id']
        # получили ид пользователя, который начал общение
        return user_id
    # вернул мой id vk

def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)
    response = upload.photo_messages(f)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    # print(owner_id, photo_id, access_key)
    # вернул
    # -213472651    457239152    7dc8d1f4a3986c418f
    # -213472651    457239153    0e7fc73c938545faaf
    # -213472651    457239154    8a9b971bb74e88662f
    return owner_id, photo_id, access_key

def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.method('messages.send', {'random_id':get_random_id(),'peer_id':peer_id,'attachment':attachment})


def vk_bot_message(foto):
        for i in range(3):
            send_photo(vk, PEER_ID, *upload_photo(upload, foto[i]))



def vk_add_button(user_id,user_search):
    k = 0

    def next_user(k):
        fio_str = vk_client.user_id_search(user_search[1][k])
        foto = vk_client.photo_laik(user_search[1][k])
        # print(foto)
        # вернул
        # [{'type': 'photo',
        #   'photo': 'https://sun9-2.userapi.com/s/v1/if2/QirM-n92xgk5hVp7cNRAUvfLDFb502Jmcf4VJVgEZXUftAXXAfBgvJx7OfN2w4S5Z1O_PokPfYeenw25gjFZ_EyB.jpg?size=1280x719&quality=96&type=album'},
        #  {'type': 'photo',
        #   'photo': 'https://sun9-21.userapi.com/s/v1/if1/JqKuDH_naazza7dQkOFcDZUMNkzzyi9N0pDAloGhCwRKtoW1GwRJXHs9h9kMW9oUt-MnKBiN.jpg?size=1024x683&quality=96&type=album'},
        #  {'type': 'photo', 'photo': 'https://sun9-67.userapi.com/c10569/u94706459/-6/z_42097e00.jpg'}]

        foto = [foto[0]['photo'], foto[1]['photo'], foto[2]['photo']]
        fio_name = fio_str[0]
        fio_last = fio_str[1]
        sait = fio_str[2]
        # next_user = fio_name +  fio_last +  sait +  foto
        # print(fio_name, fio_last, sait, foto)
        # вернул
        # Владимир Ланцов https: // vk.com / id94706459['https://sun9-2.userapi.com/s/v1/if2/QirM-n92xgk5hVp7cNRAUvfLDFb502Jmcf4VJVgEZXUftAXXAfBgvJx7OfN2w4S5Z1O_PokPfYeenw25gjFZ_EyB.jpg?size=1280x719&quality=96&type=album', 'https://sun9-21.userapi.com/s/v1/if1/JqKuDH_naazza7dQkOFcDZUMNkzzyi9N0pDAloGhCwRKtoW1GwRJXHs9h9kMW9oUt-MnKBiN.jpg?size=1024x683&quality=96&type=album', 'https://sun9-67.userapi.com/c10569/u94706459/-6/z_42097e00.jpg']

        return fio_name, fio_last, sait, foto

    def create_keyboard(response):

        keyboard = VkKeyboard(one_time=True)
        if response.lower() == ('начать' or 'старт'or 'поиск'):
            keyboard.add_button('следующий', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Парня', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('Всё равно', color=VkKeyboardColor.POSITIVE)

        else:
            keyboard.add_button('следующий', color=VkKeyboardColor.POSITIVE)

        keyboard = keyboard.get_keyboard()
        return keyboard

    # while True:
    for event in longpoll.listen():

    # event = longpoll.listen()
        if event.type == VkEventType.MESSAGE_NEW:
            print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
            print('Текст сообщения: ' + str(event.text))
            print('Id пользователя: ' + str(event.user_id))
            response = event.text.lower()
            keyboard = create_keyboard(response)
            user_id = event.user_id

            if response == 'начать':
                vk.method('messages.send',
                            {'user_id': event.user_id, 'message': 'Привет! \n'
                                                                    'Я помогу тебе найти пару или просто друзей. \n',
                               'random_id': get_random_id(),
                               'keyboard': keyboard})
            if response == 'следующий':
                #
                new_user = next_user(k)
                # print(new_user[0])
                fio_name = new_user[0]
                fio_last = new_user[1]
                sait = new_user[2]
                # print(sait)
                foto = new_user[3]
                vk.method('messages.send',
                            {'user_id': event.user_id, 'message': f'Имя: {fio_name}\n Фамилия: {fio_last}\n Страничка:{sait}\n',
                               'random_id': get_random_id(),
                               'keyboard': keyboard})
                vk_bot_message(foto)
                k += 1

        print('--------------------------------------------')



# ключ от сообщества
token = ''
vk = vk_api.VkApi(token=token)
vk._auth_token()
upload = VkUpload(vk)
PEER_ID = 
# URL = '...'
