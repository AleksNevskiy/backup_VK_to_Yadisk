from pprint import pprint
import requests
import datetime

TOKEN = ''

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
        with open('Annotation.txt', 'w') as f:
            f.write(folder_name + '\n')
        for item in annotation.items():
            params = {'path': f'{folder_name}/{item[0]}.jpg', 'url': item[1][0]}
            response = requests.post(url, headers=headers, params=params)
            if response.status_code == 202:
                print(f'Файл {item[0]} загружается')
                with open('Annotation.txt', 'a') as f:
                    f.write(str({"file_name": item[0], "size": item[1][1]}) + '\n')
            else:
                print(f'Загрузка файла {item[0]} не удалась')
        return folder_name



    def upload_annotation_to_disk(self, folder_name):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        disk_file_path = folder_name + '/Annotation.txt'
        params = {'path': disk_file_path, 'overwrite': 'false'}
        response = requests.get(upload_url, headers=headers, params=params).json()
        href = response.get('href', '')
        print(href)
        response = requests.put(href, data=open('Annotation.txt', 'rb'))
        if response.status_code == 201:
            print('Аннотация загружена')




if __name__ == '__main__':
    id = input('Введите id VK: ')
    TOKEN = input('Введите ваш токен для Яндекс.Диск: ')
    vk = VkGetData(id)
    pprint(vk.get_photos_info())
    pprint(vk.creating_annotation(vk.get_photos_info()))
    ya = YaUpload(TOKEN)
    print(ya.upload_annotation_to_disk(ya.upload_file_to_disk(vk.creating_annotation(vk.get_photos_info()))))
    # 552934290 id тестового аккаунта