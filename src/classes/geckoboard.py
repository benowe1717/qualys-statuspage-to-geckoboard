#!/usr/bin/env python3
import requests

from src.classes.file_checker import FileChecker
from src.constants import constants


class GeckboardApi:
    CREDENTIAL_KEYS = constants.GECKOBOARD_CREDENTIALS_KEYS
    SCHEME = constants.GECKOBOARD_API_SCHEME

    def __init__(self, credentials_file: str) -> None:
        self.credentials_file = credentials_file
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self._auth()

    @property
    def credentials_file(self) -> str:
        return self._credentials_file

    @credentials_file.setter
    def credentials_file(self, filepath: str) -> None:
        self._credentials_file = ''
        fc = FileChecker(filepath)
        if not fc.is_file():
            raise ValueError('Not a file')

        if not fc.is_readable():
            raise ValueError('Not readable')

        data = fc.is_yaml()
        if not data:
            raise ValueError('Not YAML')

        try:
            credentials = data['credentials']  # type: ignore
            self._credentials_file = fc.file
            self.credentials = credentials['geckoboard']
        except KeyError:
            raise ValueError('Invalid credentials file')

    @property
    def credentials(self) -> dict:
        return self._credentials

    @credentials.setter
    def credentials(self, data: dict) -> None:
        self._credentials = {}
        if len(data) != 3:
            raise ValueError('Invalid credentials file')

        for key in self.CREDENTIAL_KEYS:
            if key not in data.keys():
                raise ValueError(f'Missing {key}')

        self._credentials = data

    def _auth(self) -> None:
        self.apikey = self._credentials['apikey']
        self.widgetkey = self._credentials['widgetkey']
        self.headers['Host'] = self._credentials['host']

    def build_msg(
            self,
            status: str,
            platform_name=None,
            product_name=None) -> str | bool:
        if status.lower() == 'ok':
            msg = '<center style="background-color: green;">'
            msg += '<strong>OK</strong></center>'
            return msg

        elif status.lower() == 'down':
            msg = '<span style="background-color: red;">'
            msg += f'{platform_name} - {product_name} is <strong>DOWN!'
            msg += '</strong></span>\n\n'
            return msg

        else:
            return False

    def push_to_widget(self, msg: str) -> bool:
        endpoint = f'/v1/send/{self.widgetkey}'
        url = self.SCHEME + self.headers['Host'] + endpoint
        payload = {
            'api_key': self.apikey,
            'data': {
                'item': [{
                    'text': msg,
                    'type': 1
                }]
            }
        }
        r = requests.post(url=url, headers=self.headers, data=payload)
        if r.status_code != 200:
            error = (payload, r.status_code, r.json())
            print(error)
            return False
        return True
