import requests
import os


ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REDIRECT_URI = os.environ['REDIRECT_URI']
ABSOLUTE_PATH = os.environ['ABSOLUTE_PATH']

headers = {'Accept-Version': 'v1',
           'Authorization': f'Client-ID {ACCESS_KEY}'}

base_url = 'https://api.unsplash.com/'


def get_random_beer():
    return_dict = {}
    data = requests.get('https://api.punkapi.com/v2/beers/random')
    full_data = data.json()
    return_dict['name'] = full_data[0]['name']
    return_dict['description'] = full_data[0]['description']
    return return_dict


def get_beer_image(name):
    params = {'query': name,
              'per_page': 1}
    res = requests.get(base_url+'/search/photos',
                       params=params, headers=headers)
    data = res.json()
    download_link = data['results'][0]['links']['download']
    print(download_link)
    data_image = requests.get(download_link)
    with open('page_image.jpeg', 'wb') as f:
        f.write(data_image.content)
    return data


if __name__ == '__main__':
    name = get_random_beer()['name']
    get_beer_image(name)
