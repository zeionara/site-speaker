import json
import traceback
from time import sleep
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

HEADERS = {
    'cache-control': 'max-age=0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7'
}
http_error_delay = 5


def send_query(url: str, headers: dict, data: str = None):
    return urlopen(
        Request(
            url=url,
            headers=headers,
            data=None if data is None else data.encode()
        )
    ).read().decode(encoding='utf-8', errors='ignore')


def query(url: str, as_json: bool = False, as_html: bool = False):
    assert not (as_json and as_html)
    result = None
    while True:
        try:
            result = send_query(url=url, headers=HEADERS)
            break
        except Exception:
            print(f'Oops, an exception occurred:')
            print(traceback.format_exc())
            print(f'Error sending query. Retrying after {http_error_delay} seconds...')
            sleep(http_error_delay)

    return {} if result is None else (
        json.loads(result) if as_json else
        BeautifulSoup(result, features="html.parser") if as_html else result
    )
