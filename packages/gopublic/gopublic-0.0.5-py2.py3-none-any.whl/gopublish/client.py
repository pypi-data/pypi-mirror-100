from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from future import standard_library

from gopublish.exceptions import GopublishApiError, GopublishConnectionError, GopublishNotImplementedError

import requests

standard_library.install_aliases()


class Client(object):
    """
    Base client class implementing methods to make queries to the server
    """

    def __init__(self, url, endpoints, gopublish_mode):
        self.url = url
        self.endpoints = endpoints
        self.gopublish_mode = gopublish_mode

    def _api_call(self, call_type, endpoint_name, body={}, inline=False, headers=None):

        url = self._format_url(call_type, endpoint_name, body)

        try:
            if call_type in ["get", "delete"]:
                if inline:
                    r = requests.get(url, params=body, headers=headers)
                else:
                    r = requests.get(url, headers=headers)
            elif call_type == "post":
                r = requests.post(url, json=body, headers=headers)

            if 400 <= r.status_code <= 499:
                raise GopublishApiError("API call returned the following error: '{}'".format(r.json()['error']))
            elif r.status_code == 502:
                raise GopublishApiError("Unknown server error")
            else:
                return r.json()

        except requests.exceptions.RequestException:
            raise GopublishConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))

    def _format_url(self, call_type, endpoint_name, body, inline=False):

        endpoint = self.endpoints.get(endpoint_name)
        if not endpoint:
            raise GopublishNotImplementedError()

        # Fill parameters in the url
        if not inline and call_type in ["get", "delete"]:
            groups = re.findall(r'<(.*?)>', endpoint)
            for group in groups:
                if group not in body:
                    raise GopublishApiError("Missing get parameter " + group)
                endpoint = endpoint.replace("<{}>".format(group), body.get(group))

        return "{}{}".format(self.url, endpoint)
