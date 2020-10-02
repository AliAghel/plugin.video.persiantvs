from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import requests
from utils import *
import logging
import os.path

logger = logging.getLogger(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
TELEWEBION_PATH = os.path.join(THIS_DIR, 'data', 'telewebion.pkl')


def static_channels_list():
    return ['tv1', 'tv2', 'tv3', 'irinn', 'varzesh']


def get_all_channels():
    # base url of all channels in telewebion
    base_url = "https://www.telewebion.com/channels"

    try:
        session = requests.Session()

        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        response = session.get(base_url,
                               headers={'user-agent': 'my-app',
                                        'referer': 'https://www.telewebion.com',
                                        'origin': 'https://www.telewebion.com',
                                        'cache-control': 'no-cache'}
                               )

        # throw exception if request does not return 2xx
        response.raise_for_status()

        channels_url_content = response.content

        # BeautifulSoup object
        soup = BeautifulSoup(channels_url_content, features="html.parser")

        # create a list of all channels
        all_channels_list = [a['href'].split('/')[-1]
                             for a in soup.select('.box.h-100.pointer.d-block')]

        if len(all_channels_list) == 0:
            return ['tv1', 'tv2', 'tv3', 'irinn', 'varzesh']
        else:
            return all_channels_list

    except requests.exceptions.HTTPError as e:
        return "HTTP Error: " + str(e)
    except requests.exceptions.ConnectionError as e:
        return "Connection Error: " + str(e)
    except requests.exceptions.Timeout as e:
        return "Timeout Error: " + str(e)
    except requests.exceptions.RequestException as e:
        return "Whoops! Something went wrong: " + str(e)


def make_request(channels_name):
    base_url = 'https://w32.telewebion.com/v3/channels/{}/details?device=desktop&logo_version=4&thumb_size=240&'.format(
        channels_name)

    session = requests.Session()

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(base_url,
                           headers={'user-agent': 'my-app',
                                    'referer': 'https://www.telewebion.com/live/' + channels_name,
                                    'origin': 'https://www.telewebion.com',
                                    'cache-control': 'no-cache', }
                           )

    # return response request data as json
    return response.json()


def one_channel_list(response):
    channel_name = response['data'][0]['channel']['descriptor']
    channel_thumb = 'https://static.televebion.net/web/content_images/channel_images/thumbs/new/240/v4/{}.png'.format(
        channel_name)
    # get channel's links with different bit rates
    channel_videos = [item['link']for item in response['data'][0]['links']]

    links = []
    for v in channel_videos:
        if ('1500k.stream' in v):
            channel_video = v
            name1500 = channel_name + '(1500K)'
            links.append({'name': name1500, 'thumb': channel_thumb,
                          'video': channel_video, 'genre': 'IRIBTV'})
        elif ('1000k.stream' in v):
            channel_video = v
            name1000 = channel_name + '(1000K)'
            links.append({'name': name1000, 'thumb': channel_thumb,
                          'video': channel_video, 'genre': 'IRIBTV'})
        elif ('500k.stream' in v):
            channel_video = v
            name500 = channel_name + '(500K)'
            links.append({'name': name500, 'thumb': channel_thumb,
                          'video': channel_video, 'genre': 'IRIBTV'})

    return links


def create_telewebion_object():
    lst = []
    for c in static_channels_list():
        for link in one_channel_list(make_request(c)):
            try:
                lst.append(link)
            except (ValueError, KeyError):
                logger.exception('Failed to add %s channel!' % c)

    return lst


def telewebion():
    # if is_object_exists(TELEWEBION_PATH):
    #     telewebion = load_existing_object(TELEWEBION_PATH)
    #     try:
    #         return telewebion
    #     except (ValueError, KeyError):
    #         logger.exception('Loaded TELEWEBION object does not work!')

    # Create new object
    telewebion = create_telewebion_object()
    # Save new model
    # save_object(telewebion, TELEWEBION_PATH)
    return telewebion


print(telewebion())