from __future__ import unicode_literals
from lib.youtube_dl import YoutubeDL
from utils import *
import logging
import os.path

logger = logging.getLogger(__name__)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
BBCPERSIAN_PATH = os.path.join(THIS_DIR, 'data', 'bbcpersian.pkl')


def create_bbcpersian_object():
    try:
        bbc_live_url = 'https://www.youtube.com/watch?v=TE5d4omulHg'
        ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s',
                         'format': 'best',
                         'quiet': True,
                         'no_color': True,
                         'no_warnings': True,
                         'hls_prefer_native': True
                         })
        with ydl:
            result = ydl.extract_info(bbc_live_url, download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result

        bbcpersian_video = video['url']

        bbcpersian_object = {
            'name': 'BBC PERSIAN',
            'thumb': 'http://www.bbc.co.uk/news/special/2015/newsspec_11063/persian_1024x576.png',
            'video': bbcpersian_video,
            'genre': 'NEWS'
        }

        return bbcpersian_object

    except (ValueError, KeyError):
        logger.exception('Failed to create BBC PERSIAN object!')


def bbcpersian():
    if is_object_exists(BBCPERSIAN_PATH):
        try:
            logger.info('BBC PERSIAN object loaded successfully!')
            bbcpersian = load_existing_object(BBCPERSIAN_PATH)
            return bbcpersian
        except (ValueError, KeyError):
            logger.exception('Loaded BBC PERSIAN object does not work!')
            # Create new object
            bbcpersian = create_bbcpersian_object()
            # Save new model
            save_object(bbcpersian, BBCPERSIAN_PATH)
            return bbcpersian


print(bbcpersian())