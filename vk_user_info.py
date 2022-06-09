import requests
from datetime import date

token = ''

class VkUser:   
    url_api_vk = 'https://api.vk.com/method/'
    def __init__(self,token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }
    def user(self, user_id=None):
        url_use = self.url_api_vk + 'users.get'
        params = {
            'user_ids': user_id,
            'access_token': token,
            'fields': 'city,bdate,sex',
            'v': '5.131'
        }
        req = requests.get(url_use, params=params).json()
        rdata = req['response'][0]['bdate'].split('.')
        birth_date = date(int(rdata[2]), int(rdata[1]), int(rdata[0]))
        req_data = (date.today() - birth_date).days // 365.2425
        
        #записываю в бд (9930, 1, 33)
        
        return req['response'][0]['city']['id'],req['response'][0]['sex'], int(req_data)


    def user_id_search(self, user_id=None):
        url_use = self.url_api_vk + 'users.get'
        params = {
            'user_ids': user_id,
            'access_token': token,
            'fields': 'city,bdate,sex',
            'v': '5.131'
        }
        req = requests.get(url_use, params=params).json()
        first_name = req['response'][0]['first_name']
        last_name = req['response'][0]['last_name']
        url_user = f'https://vk.com/id{user_id}'

        return first_name, last_name, url_user


    def users_search(self,  id_city, sex, data):
        url_use = self.url_api_vk + 'users.search'
        age_from = data - 2
        age_to = data + 2
        if sex == 1:
            sex_new = 2
        elif sex == 2:
            sex_new = 1
        else:
            print('выберите пол')
        params = {
            'city': id_city,
            'sex': sex_new,
            'age_from': age_from,
            'age_to': age_to,
            'count': '1000',
            'access_token': token,
            'fields': 'id,city,friend_status',
            'v': '5.131'
        }
        req = requests.get(url_use, params=params).json()
        count_user = req['response']['count']
        id_ = req['response']['items']
        # print(id_)
        count_user_list = []
        for i in range(len(id_)):
            if id_[i]['friend_status'] == 0:
                count_user_list.append(id_[i]['id'])
        return  count_user, count_user_list

    def photo_laik(self,user_id=None):
        url_photos = self.url_api_vk + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'count': 10,
            'photo_sizes': 1
        }
        req = requests.get(url_photos, params={**self.params, **photos_params}).json()['response']['items']
        list_req = sorted(req, key=lambda user: user['likes']['count'],reverse=True)
        if len(list_req) > 2:
            foto1 = list_req[0]['sizes'][-1]['url']
            foto2 = list_req[1]['sizes'][-1]['url']
            foto3 = list_req[2]['sizes'][-1]['url']
        elif len(list_req) == 2:
            foto1 = list_req[0]['sizes'][-1]['url']
            foto2 = list_req[1]['sizes'][-1]['url']
            foto3 = None
        elif len(list_req) == 1:
            foto1 = list_req[0]['sizes'][-1]['url']
            foto2 = None
            foto3 = None
        list_photo = [{"type": "photo","photo": foto1}, {"type": "photo","photo": foto2}, {"type": "photo","photo": foto3}]
        return list_photo