#!/usr/bin/env python3
import requests

from src.classes.file_checker import FileChecker
from src.constants import constants


class StatusPageApi:
    CREDENTIAL_KEYS = constants.STATUSPAGE_CREDENTIALS_KEYS
    SCHEME = constants.STATUSPAGE_API_SCHEME

    def __init__(self, credentials_file: str) -> None:
        self.credentials_file = credentials_file
        self.pageid = ''
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self._auth()
        self.platforms = []
        self.incidents = []

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
            self.credentials = credentials['statuspage']
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
        host = self.credentials['host']
        apikey = self.credentials['apikey']
        self.headers['Host'] = host
        self.headers['Authorization'] = f'OAuth {apikey}'
        self.pageid = self.credentials['pageid']

    def get_component_groups(self) -> bool:
        endpoint = f'/v1/pages/{self.pageid}/component-groups'
        url = self.SCHEME + self.headers['Host'] + endpoint
        r = requests.get(url=url, headers=self.headers)
        if r.status_code != 200:
            error = (url, r.status_code, r.json())
            print(error)
            return False
        platforms = r.json()
        for platform in platforms:
            id = platform['id']
            name = platform['name']
            self.platforms.append((id, name))
        return True

    def get_unresolved_incidents(self) -> bool:
        endpoint = f'/v1/pages/{self.pageid}/incidents/unresolved'
        url = self.SCHEME + self.headers['Host'] + endpoint
        r = requests.get(url=url, headers=self.headers)
        if r.status_code != 200:
            error = (url, r.status_code, r.json())
            print(error)
            return False
        self.incidents = r.json()
        return True
