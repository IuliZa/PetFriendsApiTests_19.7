from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password


pf = PetFriends()

#__________________Positive Tests________________

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pets_with_valid_key(name='Minor', animal_type='animal', age='2', pet_photo='images/chameleon.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pets_with_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Minor", "animal", "2", "images/chameleon.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pets_with_valid_key(name='Major', animal_type='human',age='100'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("You haven't got any pets in your list")

#__________________Negative Tests________________


def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    ''' Запрос ключа для  пользователя c неправильно указанным email возвращает
        статус ошибки 4хх'''

    status, result = pf.get_api_key(email, password)
    assert status >= 400


def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    ''' Запрос ключа для  пользователя c неправильно указанным password возвращает
        статус ошибки 4хх'''

    status, result = pf.get_api_key(email, password)
    assert status >= 400


def test_get_all_pets_with_invalid_key(filter=''):
    '''Запрос списка животных по неверно указанному ключу возвращает
        статус ошибки 4хх'''

    auth_key = 'ea738148a1f19838e1c5d14'
    status, result = pf.get_list_of_pets_wrong(auth_key, filter)
    print(result)
    assert status >= 400


def test_add_new_pets_with_invalid_name_data(name='@!&=+', animal_type='animal', age='2', pet_photo='images/chameleon.jpg'):
    '''Добавление питомца с невалидным значением имени'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_empty_animal_type_data(name='Woodoo', animal_type=' ', age='1', pet_photo='images/chameleon.jpg'):
    '''Добавление питомца с пустым типом животного'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_long_age_data(name='Woodoo', animal_type='Chmeleon', age='1234567890', pet_photo='images/chameleon.jpg'):
    '''Добавление питомца с указанием не реального возраста'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_negative_age_data(name='Woodoo', animal_type='Chmeleon', age='-100', pet_photo='images/chameleon.jpg'):
    '''Добавление питомца с указанием отрицательного значения возраста'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_delete_pet_with_invalid_pet_id():
    '''Удаление питомца с некорректным id'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = 'af0000000000000'
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)
    assert status == 400


def test_add_new_pet_with_invalid_pet_photo_format(name='Woodoo', animal_type='Chameleon', age='2', pet_photo='images/pet.txt'):
    '''Добавление питомца с некорректным типом файла изображения'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_create_pet_simple_without_any_info(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
