from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

from gopublish.exceptions import GopublishConnectionError
from gopublish.file import FileClient
from gopublish.token import TokenClient

import requests

standard_library.install_aliases()


class GopublishInstance(object):

    def __init__(self, url="http://localhost:80", **kwargs):

        url = url.rstrip().rstrip("/")
        self.url = url

        self.gopublish_version, self.gopublish_mode = self._get_status()

        self.endpoints = self._get_endpoints()

        # Initialize Clients
        args = (self.url, self.endpoints, self.gopublish_mode)
        self.file = FileClient(*args)
        self.token = TokenClient(*args)

    def __str__(self):
        return '<GopublishInstance at {}>'.format(self.url)

    def _get_status(self):

        try:
            r = requests.get("{}/api/status".format(self.url))
            if not r.status_code == 200:
                raise requests.exceptions.RequestException
            return (r.json()["version"], r.json()["mode"])
        except requests.exceptions.RequestException:
            raise GopublishConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))

    def _get_endpoints(self):

        try:
            r = requests.get("{}/api/endpoints".format(self.url))
            if not r.status_code == 200:
                raise requests.exceptions.RequestException
            return r.json()
        except requests.exceptions.RequestException:
            raise GopublishConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))
