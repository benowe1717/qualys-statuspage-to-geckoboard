#!/usr/bin/env python3
import os

import pytest

from src.classes.geckoboard import GeckboardApi


class TestStatusPageApi:
    def setUp(self):
        self.credentials_file = 'tests/data/credentials.yaml'
        self.geckoboard = GeckboardApi(self.credentials_file)

    def tearDown(self):
        del self.geckoboard
        del self.credentials_file

    def test_missing_credentials_file(self):
        file = '/some/fake/file'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_invalid_credentials_file_not_a_file(self):
        file = '~/Documents/'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_invalid_credentials_file_not_readable(self, monkeypatch):
        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)
        file = 'tests/data/credentials.yaml'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_invalid_credentials_file_not_yaml(self):
        file = 'tests/data/not_yaml.yaml'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_invalid_credentials_file_invalid_file(self):
        file = 'tests/data/invalid_credentials.yaml'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_invalid_credentials_file_missing_key(self):
        file = 'tests/data/missing_credentials.yaml'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_invalid_credentials_file_additional_data(self):
        file = 'tests/data/additional_credentials.yaml'
        with pytest.raises(ValueError):
            GeckboardApi(file)

    def test_credentials_file(self):
        self.setUp()
        assert self.geckoboard.credentials_file == os.path.realpath(
            self.credentials_file)
        assert len(self.geckoboard.credentials) == 3
        assert 'apikey' in self.geckoboard.credentials.keys()
        assert 'host' in self.geckoboard.credentials.keys()
        assert 'widgetkey' in self.geckoboard.credentials.keys()
        self.tearDown()

    def test_headers(self):
        self.setUp()
        assert len(self.geckoboard.headers) == 3
        assert 'Content-Type' in self.geckoboard.headers.keys()
        assert 'Accept' in self.geckoboard.headers.keys()
        assert 'Host' in self.geckoboard.headers.keys()
        assert self.geckoboard.headers['Content-Type'] == 'application/json'
        assert self.geckoboard.headers['Accept'] == 'application/json'
        assert self.geckoboard.headers['Host'] == 'push.geckoboard.com'
        self.tearDown()

    def test_apikey(self):
        self.setUp()
        assert self.geckoboard.apikey == 'apikeygoeshere'
        self.tearDown()

    def test_widgetkey(self):
        self.setUp()
        assert self.geckoboard.widgetkey == 'some-widget-key-goes-here'
        self.tearDown()

    def test_build_msg_failed(self):
        self.setUp()
        status = 'UP'
        platform_name = 'US Platform 1'
        product_name = 'VMDR'
        result = self.geckoboard.build_msg(status, platform_name, product_name)
        assert result is False
        self.tearDown()

    def test_build_msg_ok(self):
        self.setUp()
        status = 'OK'
        result = self.geckoboard.build_msg(status)
        msg = '<center style="background-color: green;"><strong>'
        msg += 'OK</strong></center>'
        assert result == msg
        self.tearDown()

    def test_build_msg_down(self):
        self.setUp()
        status = 'Down'
        platform_name = 'US Platform 1'
        prodouct_name = 'VMDR'
        result = self.geckoboard.build_msg(
            status, platform_name, prodouct_name)
        msg = '<span style="background-color: red;">'
        msg += f'{platform_name} - {prodouct_name} is <strong>DOWN!</strong>'
        msg += '</span>\n\n'
        assert result == msg
        self.tearDown()

    def test_push_to_widget_failed_unauthenticated(self, requests_mock):
        self.setUp()
        widgetkey = self.geckoboard.widgetkey
        apikey = self.geckoboard.apikey
        host = self.geckoboard.headers['Host']
        endpoint = f'/v1/send/{widgetkey}'
        url = f'https://{host}{endpoint}'
        payload = {
            'apikey': 'fakekey',
            'data': {
                'items': [{
                    'text': 'some text',
                    'type': 1
                }]
            }
        }
        code = 401
        msg = '<center style="background-color: green;"><strong>'
        msg += 'OK</strong></center>'
        with open('tests/data/geckoboard_401_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('POST', url, text=data, status_code=code)
        result = self.geckoboard.push_to_widget(msg)
        assert result is False
        self.tearDown()

    def test_push_to_widget_failed_does_not_exist(self, requests_mock):
        self.setUp()
        widgetkey = self.geckoboard.widgetkey
        apikey = self.geckoboard.apikey
        host = self.geckoboard.headers['Host']
        endpoint = f'/v1/send/{widgetkey}'
        url = f'https://{host}{endpoint}'
        payload = {
            'apikey': apikey,
            'data': {
                'items': [{
                    'text': 'some text',
                    'type': 1
                }]
            }
        }
        code = 404
        msg = '<center style="background-color: green;"><strong>'
        msg += 'OK</strong></center>'
        with open('tests/data/geckoboard_404_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('POST', url, text=data, status_code=code)
        result = self.geckoboard.push_to_widget(msg)
        assert result is False
        self.tearDown()

    def test_push_to_widget(self, requests_mock):
        self.setUp()
        widgetkey = self.geckoboard.widgetkey
        apikey = self.geckoboard.apikey
        host = self.geckoboard.headers['Host']
        endpoint = f'/v1/send/{widgetkey}'
        url = f'https://{host}{endpoint}'
        payload = {
            'apikey': apikey,
            'data': {
                'items': [{
                    'text': 'some text',
                    'type': 1
                }]
            }
        }
        code = 200
        msg = '<center style="background-color: green;"><strong>'
        msg += 'OK</strong></center>'
        with open('tests/data/push_to_widget.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('POST', url, text=data, status_code=code)
        result = self.geckoboard.push_to_widget(msg)
        assert result is True
        self.tearDown()
