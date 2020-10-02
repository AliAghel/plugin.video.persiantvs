from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import requests


def get_radiojavan_video():
    try:
        base_url = "https://www.radiojavan.com/tv"

        session = requests.Session()

        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        response = session.get(base_url,
                               headers={'user-agent': 'my-app',
                                        'referer': 'https://www.radiojavan.com/',
                                        'origin': 'https://www.radiojavan.com/',
                                        'cache-control': 'no-cache',
                                        'Content-Type': 'application/json'}
                               )

        # throw exception if request does not return 2xx
        response.raise_for_status()

        content = response.content

        # BeautifulSoup object
        soup = BeautifulSoup(content, features="html.parser")

        source = 'http:' + soup.find_all("source")[0]['src']
        return source

    except requests.exceptions.HTTPError as e:
        return "HTTP Error: " + str(e)
    except requests.exceptions.ConnectionError as e:
        return "Connection Error: " + str(e)
    except requests.exceptions.Timeout as e:
        return "Timeout Error: " + str(e)
    except requests.exceptions.RequestException as e:
        return "Whoops! Something went wrong: " + str(e)