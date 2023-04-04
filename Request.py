from pprint import pprint
import json
import requests
from reddit import Reddit
from ya_disk import YandexDisk

TOKEN = ""

def test_request():
    url = "https://bootssizes/get"
    params = {"model": "nike123"}
    headers = {"Authorization": "secret - token - 123"}
    response = requests.get(url, params=params, headers=headers, timeout=5)
    pprint(response)

def most_intelligence_hero(hero_list):
    url = "https://akabab.github.io/superhero-api/api/all.json"
    resp = requests.get(url)
    data = resp.json()
    all_powerstats = {}
    for dict in data:
        if dict['name'] in hero_list:
            stats = dict['powerstats'] 
            intel = stats['intelligence']
            all_powerstats[dict['name']] = intel
    most_intel = (max(all_powerstats, key=all_powerstats.get))
    return most_intel

hero = ['Hulk', 'Captain America', 'Thanos']
print(f'Самый умный супергерой: {most_intelligence_hero(hero)}.')

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data['href']
        return href
    
    def upload_file_to_disk(self, disk_file_path, filename):
        """Метод загружает файл на яндекс диск"""
        href = self._get_upload_link(disk_file_path = disk_file_path)
        response = requests.put(href, data=open(filename, 'rb'))
        if response.status_code == 201:
            print("Файл загружен.")


# if __name__ == '__main__':
#     path_to_file = 'python/all_json.json'
#     token = TOKEN
#     upload_file_to_disk = YaUploader(token)
#     result = upload_file_to_disk.upload_file_to_disk(path_to_file, 'all_json.json')