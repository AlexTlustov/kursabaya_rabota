
import requests
import logging
import datetime
# Создал логгер
log_module = logging.getLogger('Vkontakte')
# Функция поиска картники с максимальным расширением
def find_max_dpi(dict_in_search):
    max_dpi = 0
    need_elem = 0
    for j in range(len(dict_in_search)):
        file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            need_elem = j
    log_module.debug('The maximum size of the photo and its link were found.')
    return dict_in_search[need_elem].get('url'), dict_in_search[need_elem].get('type') 
# Функция преоброзования UNIX TIME в обычную дату и время.
def time_convert(time_unix):
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    log_module.debug('Conversion of UNIX time to a normal date.')
    return str_time

class VkRequest:
    # Авторизация в ВК
    def __init__(self, token_list, version='5.131'):
        self.token = token_list[0]
        self.id = token_list[1]
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self._sort_info()
        self.logger = logging.getLogger('log.Vkontakte.VkRequest')
        self.logger.info('The main parameters for the VK request have been obtained.')
    # Получение словарей с информацией о фотографиях пользователя
    def _get_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1,
                  'rev': 1
                  }
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']
        self.logger = logging.getLogger('log.Vkontakte.VkRequest')
        self.logger.info('All information about the photos has been received.') 
        return photo_info['count'], photo_info['items']
    # Получение словаря с количеством лайком, именем(в качестве дата и время), ссылке на фото, размер.  
    def _get_logs_only(self):
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = find_max_dpi(photo_items[i]['sizes'])
            time_warp = time_convert(photo_items[i]['date'])
            new_value = result.get(likes_count, [])
            new_value.append({'likes_count': likes_count,
                              'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value  
        self.logger = logging.getLogger('log.Vkontakte.VkRequest')
        self.logger.info('The parameters of the photos were obtained.')     
        return result
    # Сортировка и фильтрация информации о фото, создаем JSON и словрь с ключем (имя файла), значение (ссылка на фото)
    def _sort_info(self):
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        counter = 0
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{value["likes_count"]}.jpeg'
                else:
                    file_name = f'{value["likes_count"]} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                if value["likes_count"] == 0:
                    sorted_dict[file_name] = picture_dict[elem][counter]['url_picture']
                    counter += 1
                else:
                    sorted_dict[file_name] = picture_dict[elem][0]['url_picture']   
        self.logger = logging.getLogger('log.Vkontakte.VkRequest')
        self.logger.info('')                      
        return json_list, sorted_dict





