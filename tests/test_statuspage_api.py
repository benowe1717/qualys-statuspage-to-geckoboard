#!/usr/bin/env python3
import os

import pytest

from src.classes.statuspage_api import StatusPageApi


class TestStatusPageApi:
    def setUp(self):
        self.credentials_file = 'tests/data/credentials.yaml'
        self.statuspage = StatusPageApi(self.credentials_file)

    def tearDown(self):
        del self.statuspage
        del self.credentials_file

    def test_missing_credentials_file(self):
        file = '/some/fake/file'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_invalid_credentials_file_not_a_file(self):
        file = '~/Documents/'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_invalid_credentials_file_not_readable(self, monkeypatch):
        def mock_return(path, mode):
            return False
        monkeypatch.setattr(os, 'access', mock_return)
        file = 'tests/data/credentials.yaml'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_invalid_credentials_file_not_yaml(self):
        file = 'tests/data/not_yaml.yaml'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_invalid_credentials_file_invalid_file(self):
        file = 'tests/data/invalid_credentials.yaml'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_invalid_credentials_file_missing_key(self):
        file = 'tests/data/missing_credentials.yaml'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_invalid_credentials_file_additional_data(self):
        file = 'tests/data/additional_credentials.yaml'
        with pytest.raises(ValueError):
            StatusPageApi(file)

    def test_credentials_file(self):
        self.setUp()
        assert self.statuspage.credentials_file == os.path.realpath(
            self.credentials_file)
        assert len(self.statuspage.credentials) == 3
        assert 'apikey' in self.statuspage.credentials.keys()
        assert 'host' in self.statuspage.credentials.keys()
        assert 'pageid' in self.statuspage.credentials.keys()
        self.tearDown()

    def test_headers(self):
        self.setUp()
        assert len(self.statuspage.headers) == 4
        assert 'Content-Type' in self.statuspage.headers.keys()
        assert 'Accept' in self.statuspage.headers.keys()
        assert 'Host' in self.statuspage.headers.keys()
        assert 'Authorization' in self.statuspage.headers.keys()
        assert self.statuspage.headers['Content-Type'] == 'application/json'
        assert self.statuspage.headers['Accept'] == 'application/json'
        assert self.statuspage.headers['Host'] == 'api.statuspage.io'
        assert self.statuspage.headers['Authorization'] == 'OAuth some-api-key-goes-here'
        self.tearDown()

    def test_pageid(self):
        self.setUp()
        assert self.statuspage.pageid == 'ra5h7xd8knxz'
        self.tearDown()

    def test_get_component_groups_failed_unauthenticated(self, requests_mock):
        self.setUp()
        pageid = self.statuspage.pageid
        host = self.statuspage.headers['Host']
        endpoint = f'/v1/pages/{pageid}/component-groups'
        url = f'https://{host}{endpoint}'
        code = 401
        with open('tests/data/401_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('GET', url, text=data, status_code=code)
        result = self.statuspage.get_component_groups()
        assert result is False
        assert len(self.statuspage.platforms) == 0
        self.tearDown()

    def test_get_component_groups_failed_not_found(self, requests_mock):
        self.setUp()
        pageid = self.statuspage.pageid
        host = self.statuspage.headers['Host']
        endpoint = f'/v1/pages/{pageid}/component-groups'
        url = f'https://{host}{endpoint}'
        code = 401
        with open('tests/data/404_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('GET', url, text=data, status_code=code)
        result = self.statuspage.get_component_groups()
        assert result is False
        assert len(self.statuspage.platforms) == 0
        self.tearDown()

    def test_get_component_groups(self, requests_mock):
        self.setUp()
        pageid = self.statuspage.pageid
        host = self.statuspage.headers['Host']
        endpoint = f'/v1/pages/{pageid}/component-groups'
        url = f'https://{host}{endpoint}'
        code = 200
        with open('tests/data/component_groups.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('GET', url, text=data, status_code=code)
        result = self.statuspage.get_component_groups()
        assert result is True
        assert len(self.statuspage.platforms) == 2
        platform = self.statuspage.platforms[0]
        assert isinstance(platform, tuple)
        assert platform[0] == '401j1885m96y'
        assert platform[1] == 'US Platform 1'
        self.tearDown()

    def test_get_unresolved_incidents_failed_unauthenticated(
            self, requests_mock):
        self.setUp()
        pageid = self.statuspage.pageid
        host = self.statuspage.headers['Host']
        endpoint = f'/v1/pages/{pageid}/incidents/unresolved'
        url = f'https://{host}{endpoint}'
        code = 401
        with open('tests/data/401_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('GET', url, text=data, status_code=code)
        result = self.statuspage.get_unresolved_incidents()
        assert result is False
        assert len(self.statuspage.incidents) == 0
        self.tearDown()

    def test_get_unresolved_incidents_failed_not_found(self, requests_mock):
        self.setUp()
        pageid = self.statuspage.pageid
        host = self.statuspage.headers['Host']
        endpoint = f'/v1/pages/{pageid}/incidents/unresolved'
        url = f'https://{host}{endpoint}'
        code = 404
        with open('tests/data/404_response.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('GET', url, text=data, status_code=code)
        result = self.statuspage.get_unresolved_incidents()
        assert result is False
        assert len(self.statuspage.incidents) == 0
        self.tearDown()

    def test_get_unresolved_incidents(self, requests_mock):
        self.setUp()
        pageid = self.statuspage.pageid
        host = self.statuspage.headers['Host']
        endpoint = f'/v1/pages/{pageid}/incidents/unresolved'
        url = f'https://{host}{endpoint}'
        code = 200
        with open('tests/data/unresolved_incidents.json', 'r') as file:
            data = file.read()
        requests_mock.register_uri('GET', url, text=data, status_code=code)
        result = self.statuspage.get_unresolved_incidents()
        assert result is True
        assert len(self.statuspage.incidents) == 2
        incident = self.statuspage.incidents[0]
        assert isinstance(incident, dict)
        assert 'id' in incident.keys()
        assert incident['id'] == 'ccjn0q5gtl8h'
        self.tearDown()
