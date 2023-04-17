import os
import logging
import json
from YaDisk import Yandex
from Vkontakte import VkRequest
# Настройка логирования
logging.basicConfig(level='DEBUG')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel('ERROR')
handler = logging.FileHandler(f"logs.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Получение токена и ID ВК
def get_token_id(file_name):
    with open(os.path.join(os.getcwd(), file_name), 'r') as token_file:
        token = token_file.readline().strip()
    id_one = input('Введите ID пользователя: ')
    return [token, id_one]

# Получение токена Яндекс Диск.
def get_token_ya():
    token_ya = input('Введите токен для доступа к Яндекс Диску: ')
    return token_ya

if __name__ == '__main__':
    # Чтение токенов из файлов. 
    tokenVK = 'private/vk_token.txt'  
    tokenYandex = 'private/ya_token.txt'
    id_vk = '65068947'
    # Получение ссылки и название фото. 
    my_VK = VkRequest(get_token_id(tokenVK)) 
    # Сохранение в JSON инфомрации о фото.
    with open('VK_photo.json', 'w') as outfile:  
        json.dump(my_VK.json, outfile)
    logger.info('Data is written to a file "VK_photo.json".')
    # Копирование фото на Яндекс Диск. 
    my_yandex = Yandex('VK Photo', get_token_ya(), 5)
    my_yandex.create_copy(my_VK.export_dict)  
    logger.info('Photos copied to yandex disk.')

