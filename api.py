import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email: str, password: str) -> json:
        '''Метод делает запрос к API сервера и возвращает статус запроса
        и результат в формате JSON с уникальным ключом пользователя, найденного
        по указанным email и паролю'''

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets (self, auth_key, filter):
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат
           со списком найденных питомцев, совпадающих с фильтром. На данный момент
           фильтр пустое значение- получить список всех питомцев, либо my pets-
           получить список своих питомцев'''

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name= str, animal_type= str, age= str, pet_photo= str) -> json:
        '''Метод делает запрос к API сервера, отправляет данные о питомце, добавляя его на сайт и
        возвращает статус запроса и результат -данные о добавленном питомце в формате json'''

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: json) -> json:
        '''Метод отправляет запрос к API сервера на удаление питомца и возвращает
        статус запроса и результат- данные о выполненном удалении в формате json'''

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + '/api/pets/{pet_id}' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        '''Метод отправляет запрос к API сервера и отправляет данные для добавления
        информации о существующем питомце.Возвращает статус запроса и результат
        в формате json'''

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: json, name: str , animal_type: str, age) -> json:
        '''Метод делает запрос к API сервера, отправляет данные о питомце без
        файла с фотографией , добавляя его на сайт и возвращает статус запроса
        и результат -данные о добавленном питомце в формате json'''


        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age

            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code

        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def set_pet_photo(self, auth_key: json, pet_id: json, pet_photo) -> json:
        '''Метод отправляет запрос к API сервера и отправляет данные для добавления
        фотографии в карточку  существующего питомца.Возвращает статус запроса и результат
        в формате json'''

        data = MultipartEncoder(
            fields={

                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + f'/api/pets/set_photo/{pet_id}', headers=headers, data=data)

        status = res.status_code

        result = ''
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

