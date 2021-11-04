from pprint import pprint
import requests

class VkUploader:
    def get_token(self):
        with open('token_vk.txt', 'r') as file_object:
            self.token = file_object.read().strip()
            # print(self.token)
        return self.token
    url = 'https://api.vk.com/method/'
    def __init__(self, owner_id, version='5.131'):
        self.params = {
            'access_token': self.get_token(),
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


# tests = VkUploader()
# tests.get_token()




if __name__ == '__main__':
    tests = VkUploader('552934290')
    pprint(tests.get_photos_info())
    pprint(tests.creating_annotation(tests.get_photos_info()))