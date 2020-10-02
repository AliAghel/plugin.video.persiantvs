from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from lib.youtube_dl import utils
from utils import *
import logging
import os.path

logger = logging.getLogger(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
TVA_PATH = os.path.join(THIS_DIR, 'data', 'tva.pkl')


def static_channels_list():
    return {
        'TV1':
            {'uuid': '0823beb2-f2fa-4a2c-ae37-d429a0f55d80',
             'image': 'https://s3.ott.tva.tv/rosing-tva-production/831342b5dc81d07ebec7_512x512c.png'},
        'TV2':
            {'uuid': '6fcc0a2e-1135-482c-b054-08a96e68b758',
             'image': 'https://s3.ott.tva.tv/rosing-tva-production/bec73f72f63958fc6998_512x512c.png'},
        'TV3':
            {'uuid': '0149e4b4-6027-4be9-af1d-35223920d6db',
             'image': 'https://s3.ott.tva.tv/rosing-tva-production/2768e5ba4bbed336b88e_512x512c.png'},
        'IRINN':
            {'uuid': 'ff76db87-84ff-4b94-bd6e-0656cf1b9428',
             'image': 'https://s3.ott.tva.tv/rosing-tva-production/44d0105b6c9ec94b5c3e_512x512c.png'},
        'Varzesh':
            {'uuid': '41eb32ae-00bd-4236-8ce2-c96063a35096',
             'image': 'https://s3.ott.tva.tv/rosing-tva-production/0ab89817dd01379d6156_512x512c.png'}
    }


def get_access_token():
    url = "https://api.ott.tva.tv/oauth/token?client_id=66797942-ff54-46cb-a109-3bae7c855370"
    payload = {
        "client_id": "66797942-ff54-46cb-a109-3bae7c855370",
        "client_version": "0.0.1",
        "locale": "fa-IR",
        "timezone": 7200,
        "grant_type": "password",
        "username": "989125150439",
        "password": "aam137@yahoo.com",
        "client_secret": "d0ae2c6c-d881-40ad-88f7-202d75ce0c0e"
    }

    response = requests.request("POST", url, data=payload)
    return response.json()['access_token']


def get_video(uuid):
    base_url = 'https://api.ott.tva.tv/v1/channels/{}/stream.json?audio_codec=mp4a&client_id=66797942-ff54-46cb-a109-3bae7c855370&client_version=0.0.1&device_token=7cf4df59-7c9c-40aa-97f0-38f516424038&drm=spbtvcas&locale=fa-IR&protocol=hls&screen_height=1080&screen_width=1920&timezone=7200&video_codec=h264'.format(
        uuid)

    session = requests.Session()

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    std_headers = {
        'User-Agent': utils.random_user_agent(),
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.5',
    }

    if uuid == '41eb32ae-00bd-4236-8ce2-c96063a35096':
        payload = 'access_token=' + get_access_token()
        response = session.get(base_url, headers=std_headers, params=payload)
    else:
        response = session.get(base_url, headers=std_headers)

    content = response.json()

    return content['data']['url']


def create_tva_object():
    lst = []
    for k, v in static_channels_list().items():
        try:
            channel = {'name': k,
                       'thumb': v['image'],
                       'video': get_video(v['uuid']),
                       'genre': 'IRIBTV'}
            lst.append(channel)
        except (ValueError, KeyError):
            logger.exception('Failed to add %s channel!' % k)

    return lst


def tva():
    if is_object_exists(TVA_PATH):
        tva = load_existing_object(TVA_PATH)
        try:
            return tva
        except (ValueError, KeyError):
            logger.exception('Loaded TVA object does not work!')

    # Create new object
    tva = create_tva_object()
    # Save new model
    save_object(tva, TVA_PATH)
    return tva


print(tva())
