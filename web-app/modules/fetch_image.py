import requests
from bs4 import BeautifulSoup

def get_planespotters_picture(hex_code):
    url = f'https://api.planespotters.net/pub/photos/hex/{hex_code}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            photo_info = data['photos'][0]
            return photo_info['thumbnail_large']['src']
    return None

def get_flightaware_picture(tail_number):
    url = f'https://www.flightaware.com/photos/aircraft/{tail_number}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    def get_matching_url(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tags = soup.find_all('a')
            base_url = '/photos/view/'
            for a in a_tags:
                href = a.get('href', '')
                if href.startswith(base_url) and '/aircraft/' not in href:
                    return 'https://www.flightaware.com' + href
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    def get_fullsize_image_url(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tags = soup.find_all('a', {'data-size': 'fullsize'})
            for a in a_tags:
                img_src = a.get('data-imgsrc')
                if img_src:
                    return img_src
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None

    matching_url = get_matching_url(url, headers)
    if matching_url:
        fullsize_image_url = get_fullsize_image_url(matching_url, headers)
        if fullsize_image_url:
            return fullsize_image_url
        else:
            return None
    else:
        return None


def get_aircraft_picture(hex_code, tail_number):
    planespotters_picture = get_planespotters_picture(hex_code)
    if planespotters_picture:
        return planespotters_picture
    flightaware_picture = get_flightaware_picture(tail_number)
    if flightaware_picture:
        return flightaware_picture
    return None


