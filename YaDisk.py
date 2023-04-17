import requests
import logging
from tqdm import tqdm
# Создал логгер
log_module = logging.getLogger('YaDisk')

class Yandex:
    # Метод авторизации на ЯндексДиске
    def __init__(self, folder_name, token_ya, num=5):
        self.token = token_ya
        self.added_files_num = num
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self._create_folder(folder_name)
        self.logger = logging.getLogger('log.YaDisk.Yandex')
        self.logger.info('Method for getting parameters to upload to Yandex Disk.')
    # Метод создания папки на ЯндексДиске
    def _create_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'\nПапка {folder_name} успешно создана.\n')
        else:
            print(f'\nПапка {folder_name} уже существует.\n')
        self.logger = logging.getLogger('log.YaDisk.Yandex')
        self.logger.info('Folder has been created on Yandex Disk.')    
        return folder_name
    # Метод получения ссылки для загрузки фото в папке
    def _in_folder(self, folder_name):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        in_folder_list = []
        for elem in resource:
            in_folder_list.append(elem['name'])
        self.logger = logging.getLogger('log.YaDisk.Yandex')
        self.logger.info('Received link to upload photos.') 
        return in_folder_list
    # Копирование фотографий в ЯндексДиск
    def create_copy(self, dict_files):
        files_in_folder = self._in_folder(self.folder)
        copy_counter = 0
        for key, i in zip(dict_files.keys(), tqdm(range(self.added_files_num))):
            if copy_counter < self.added_files_num:
                if key not in files_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key],
                              'overwrite': 'false'}
                    requests.post(self.url, headers=self.headers, params=params)
                    copy_counter += 1
                    self.logger = logging.getLogger('log.YaDisk.Yandex')
                    self.logger.info('Photos have been added.')
                else:
                    print(f'Внимание:Файл {key} уже существует')
                    self.logger = logging.getLogger('log.YaDisk.Yandex')
                    self.logger.info('Photos have been replaced.')
            else:
                break
        self.logger = logging.getLogger('log.YaDisk.Yandex')
        self.logger.info(f'Request completed, new files copied: {copy_counter}') 
        self.logger.info(f'Total files in the VK album: {len(dict_files)}')  