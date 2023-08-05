from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from future import standard_library

from gopublish.client import Client
from gopublish.exceptions import GopublishTokenMissingError

standard_library.install_aliases()


class FileClient(Client):
    """
    Manipulate files managed by Gopublish
    """

    def list(self, limit=None, offset=None):
        """
        List files published in Gopublish

        :type limit: int
        :param limit: Limit the results numbers

        :type offset: int
        :param offset: Offset for listing the results (used with limit)

        :rtype: dict
        :return: Dict with files and total count
        """

        body = {}

        if offset and not limit:
            offset = None
        if limit:
            body['limit'] = limit
        if offset:
            body['offset'] = offset

        return self._api_call("get", "list_files", body, inline=True)

    def search(self, file_name, limit=None, offset=None):
        """
        Launch a pull task

        :type file_name: str
        :param file_name: Either a file name, or a file UID

        :type limit: int
        :param limit: Limit the results numbers

        :type offset: int
        :param offset: Offset for listing the results (used with limit)

        :rtype: dict
        :return: Dict with files and total count
        """
        body = {"file": file_name}

        if offset and not limit:
            offset = None
        if limit:
            body['limit'] = limit
        if offset:
            body['offset'] = offset

        return self._api_call("get", "search", body, inline=True)

    def publish(self, path, version=1, contact="", email="", token=""):
        """
        Launch a publish task

        :type path: str
        :param path: Path to the file to be published

        :type version: int
        :param version: Version of the file to publish

        :type contact: str
        :param contact: Contact email for this file

        :type email: str
        :param email: Contact email for notification when publication is done

        :type token: str
        :param token: You Gopublish token.

        :rtype: dict
        :return: Dictionnary containing the response
        """
        body = {"path": path, "version": version, "contact": contact, "email": email}
        if email:
            body['email'] = email

        if contact:
            body['contact'] = contact

        if not token:
            if os.getenv("GOPUBLISH_TOKEN"):
                token = os.getenv("GOPUBLISH_TOKEN")
            else:
                raise GopublishTokenMissingError("Missing token: either specify it with --token, or set it as GOPUBLISH_TOKEN in your environnment")
        headers = {"Authorization": "Bearer " + token}

        return self._api_call("post", "publish_file", body, headers=headers)
