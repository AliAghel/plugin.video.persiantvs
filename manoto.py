from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import requests

from requests_html import HTML


def get_manoto_video():
    try:
        # base url of all channels in telewebion
        base_url = "https://www.manototv.com/live"

        session = requests.Session()

        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        response = session.get(base_url,
                               headers={'user-agent': 'my-app',
                                        'referer': 'https://www.manototv.com/',
                                        'origin': 'https://www.manototv.com/',
                                        'cache-control': 'no-cache',
                                        'Content-Type': 'application/json'}
                               )

        # throw exception if request does not return 2xx
        response.raise_for_status()

        content = response.content

        # BeautifulSoup object
        soup = BeautifulSoup(content, features="html.parser")
        html = HTML(html=content, url=base_url)
        # source = 'http:' + soup.find_all("source")[0]['src']
        return html.render()

    except requests.exceptions.HTTPError as e:
        return "HTTP Error: " + str(e)
    except requests.exceptions.ConnectionError as e:
        return "Connection Error: " + str(e)
    except requests.exceptions.Timeout as e:
        return "Timeout Error: " + str(e)
    except requests.exceptions.RequestException as e:
        return "Whoops! Something went wrong: " + str(e)


print(get_manoto_video())
