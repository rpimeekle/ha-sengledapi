"""Sengled Bulb Integration."""

import json
import logging
import ssl

import aiohttp
import certifi
import requests

from .exceptions import SengledApiAccessToken

_LOGGER = logging.getLogger(__name__)

_LOGGER.info("SengledApi: Initializing Request")


class Request:
    def __init__(self, url, payload, no_return=False):
        _LOGGER.info("SengledApi: Sengled Request initializing.")
        self._url = url
        self._payload = json.dumps(payload)
        self._no_return = no_return
        self._response = None
        self._jsession_id = None

        self._header = {
            "Content-Type": "application/json",
            "Host": "element.cloud.sengled.com:443",
            "Connection": "keep-alive",
        }

    async def async_get_response(self, jsession_id):
        self._header = {
            "Content-Type": "application/json",
            "Cookie": f"JSESSIONID={jsession_id}",
            "Connection": "keep-alive",
        }
        
        # It's important to create a new SSL context for secure HTTPS requests.
        sslcontext = ssl.create_default_context(cafile=certifi.where())

        # Use aiohttp's ClientSession for asynchronous HTTP requests.
        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, headers=self._header, data=self._payload, ssl=sslcontext) as response:
                # Make sure to handle potential exceptions and non-JSON responses appropriately.
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    # Log an error or handle the response appropriately if not successful.
                    return None

    ########################Login#####################################
    def get_login_response(self):
        _LOGGER.info("SengledApi: Get Login Reponse.")
        r = requests.post(self._url, headers=self._header, data=self._payload)
        data = r.json()
        _LOGGER.debug("SengledApi: Get Login Reponse %s", str(data))
        return data

    async def async_get_login_response(self):
        _LOGGER.info("SengledApi: Get Login Response async.")
        async with aiohttp.ClientSession() as session:
            sslcontext = ssl.create_default_context(cafile=certifi.where())
            async with session.post(
                self._url, headers=self._header, data=self._payload, ssl=sslcontext
            ) as resp:
                data = await resp.json()
                _LOGGER.debug("SengledApi: Get Login Response %s ", str(data))
                return data

    ######################Session Timeout#################################
    def is_session_timeout_response(self, jsession_id):
        _LOGGER.info("SengledApi: Get Session Timeout Response")
        self._header = {
            "Content-Type": "application/json",
            "Cookie": "JSESSIONID={}".format(jsession_id),
            "sid": jsession_id,
            "X-Requested-With": "com.sengled.life2",
        }

        r = requests.post(self._url, headers=self._header, data=self._payload)
        data = r.json()
        _LOGGER.debug("SengledApi: Get Session Timeout Response %s", str(data))
        return data

    async def async_is_session_timeout_response(self, jsession_id):
        _LOGGER.info("SengledApi: Get Session Timeout Response Async")
        self._header = {
            "Content-Type": "application/json",
            "Cookie": "JSESSIONID={}".format(jsession_id),
            "sid": jsession_id,
            "X-Requested-With": "com.sengled.life2",
        }
        async with aiohttp.ClientSession() as session:
            sslcontext = ssl.create_default_context(cafile=certifi.where())
            async with session.post(
                self._url, headers=self._header, data=self._payload, ssl=sslcontext
            ) as resp:
                data = await resp.json()
                _LOGGER.info(
                    "SengledApi: Get Session Timeout Response Async %s", str(data)
                )
                return data
