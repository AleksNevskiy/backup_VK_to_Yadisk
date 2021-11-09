from pprint import pprint
import requests
import datetime

TOKEN = 'AQAAAAAFnjqpAADLW_qlheqamk17lcRQnKPsRVE'

class VkGetData:
    def get_vk_token(self):
        with open('token_vk.txt', 'r') as file_object:
            self.vk_token = file_object.read().strip()
            # print(self.token)
        return self.vk_token
    url = 'https://api.vk.com/method/'
    def __init__(self, owner_id, version='5.131'):
        self.params = {
            'access_token': self.get_vk_token(),
            'v': version,
            'owner_id': owner_id
        }

    def get_photos_info(self):
        get_photos_url = self.url + 'photos.get'
        get_photos_params = {
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1
        }
        res = requests.get(get_photos_url, params={**self.params, **get_photos_params}).json()
        return res['response']

    def creating_annotation(self, photos_info):
        annotation = {}
        for item in photos_info['items']:
            if item['likes']['count'] in annotation.keys():
                annotation[f"{item['likes']['count']}_{item['date']}"] = [item["sizes"][-1]["url"],
                f'{item["sizes"][-1]["height"]}x{item["sizes"][-1]["width"]}']
            else:
                annotation[item['likes']['count']] = [item["sizes"][-1]["url"],
                f'{item["sizes"][-1]["height"]}x{item["sizes"][-1]["width"]}']
        return annotation


class YaUpload:
    def __init__(self, ya_token):
        self.ya_token = ya_token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }

    def create_a_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        now = datetime.datetime.now()
        date_time = f'{datetime.date.today()}_{now.hour}_{now.minute}_{now.second}'
        disk_path = f'/Vk_backup{date_time}'
        print(disk_path)
        requests.put(url, headers=headers, params={'path': disk_path})
        return disk_path

    def upload_file_to_disk(self, annotation):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        folder_name = self.create_a_folder()
        for item in annotation.items():
            params = {'path': f'{folder_name}/{item[0]}.jpg', 'url': item[1][0]}
            response = requests.post(url, headers=headers, params=params)
            if response.status_code == 202:
                print(f'Файл {item[0]} загружается')
            else:
                print(f'Загрузка файла {item[0]} не удалась')
        # print(params)





if __name__ == '__main__':
    tests = VkGetData('552934290')
    pprint(tests.get_photos_info())
    pprint(tests.creating_annotation(tests.get_photos_info()))
    test_1 = YaUpload(TOKEN)
    print(test_1.upload_file_to_disk(tests.creating_annotation(tests.get_photos_info())))