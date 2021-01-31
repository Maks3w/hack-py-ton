import warnings

import magic
import requests
from urllib3.exceptions import InsecureRequestWarning


class Crawler:
    @staticmethod
    def request(url: str) -> str:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }

        session = requests.Session()
        req = session.prepare_request(requests.Request(
            method='GET',
            url=url,
            headers=headers,
        ))
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=InsecureRequestWarning)

            resp = session.send(
                req,
                allow_redirects=False,
                verify=False,  # Don't verify SSL certificates
            )

            mime_type = magic.from_buffer(resp.content, mime=True)
            if 'text' not in mime_type:
                raise ValueError('Not HTML response')
            return resp.text
