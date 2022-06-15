from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
import vk_api
import requests
from io import BytesIO
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
from vk_user_info import VkUser
from vk_bot_base.ORM_CREATE import Searching_result, Photo

# токен сообщества
token = ''
vk = vk_api.VkApi(token=token)
vk._auth_token()
longpoll = VkLongPoll(vk)
upload = VkUpload(vk)

# токен пользователя от приложения
token1 = ''
vk_client = VkUser(token1)
searching_result = Searching_result()
photo = Photo()

def vk_bot_id_user():
    value = {
            'offset': 0,
            'count': 20,
            'filter': 'unanswered'
    }

    messages = vk.method('messages.getConversations', value)
    if messages['count'] >= 1:
        user_id = messages['items'][0]['last_message']['from_id']
        return user_id

def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)
    response = upload.photo_messages(f)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    return owner_id, photo_id, access_key

def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.method('messages.send', {'random_id':get_random_id(),'peer_id':peer_id,'attachment':attachment})


def vk_bot_message(foto, PEER_ID):
        for i in range(3):
            send_photo(vk, PEER_ID, *upload_photo(upload, foto[i]))


def vk_add_button(user_id,user_search):
    k = 0

    def next_user(k):
        fio_str = vk_client.user_id_search(user_search[1][k])
        foto = vk_client.photo_laik(user_search[1][k])
        foto = [foto[0]['photo'], foto[1]['photo'], foto[2]['photo']]
        fio_name = fio_str[0]
        fio_last = fio_str[1]
        sait = fio_str[2]
        return fio_name, fio_last, sait, foto

    def create_keyboard(response=None):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('следующий', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('добавить в избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('показать избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Отмена', color=VkKeyboardColor.POSITIVE)
        keyboard = keyboard.get_keyboard()
        return keyboard

    for event in longpoll.listen():
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
                new_user = next_user(k)
                fio_name = new_user[0]
                fio_last = new_user[1]
                sait = new_user[2]
                foto = new_user[3]
                searching_result.add_Searching_results(fio_name, fio_last, sait, user_id)
                photo.add_photo(fio_name, fio_last, foto)
                vk.method('messages.send',
                            {'user_id': event.user_id, 'message': f'Имя: {fio_name}\n Фамилия: {fio_last}\n Страничка:{sait}\n',
                               'random_id': get_random_id(),
                               'keyboard': keyboard})
                vk_bot_message(foto,user_id)
            if response == 'добавить в избранное':
                searching_result.add_fivorites(fio_name, fio_last)
                vk.method('messages.send',
                          {'user_id': event.user_id, 'message': f' {fio_name} {fio_last} добавлен/а в избранное',
                           'random_id': get_random_id(),
                           'keyboard': keyboard})
            if response == 'показать избранное':
                favorites_list = searching_result.get_fivorites(user_id)               
                count = 0
                for fav in favorites_list:
                    count += 1
                    vk.method('messages.send',
                                {'user_id': event.user_id, 'message': f'Ваше избранное:\n{count}. {fav[0]} {fav[1]}\n',
                                'random_id': get_random_id(),
                                'keyboard': keyboard})           
            k += 1
            if response == 'Отмена':
                break
    print('--------------------------------------------')