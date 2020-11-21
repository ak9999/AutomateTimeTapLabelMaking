from functools import wraps
import json

from timetappy.auth import TimeTapAuthentication
import requests


def return_response(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        response = fn(*args, **kwargs)
        if not response.status_code:
            return response.status_code
        try:
            return json.loads(response.text)
        except Exception:
            pass  # If we can't parse the JSON string for whatever reason, just skip.
    return wrapped


def api_get_request(self, url, params: dict = {}):
    api_url = self.base_url + url
    response = requests.get(url=api_url, auth=TimeTapAuthentication(self.key, self.secret, self.token), params=params)
    return response


def api_post_request(self, url, params: dict = {}):
    api_url = self.base_url + url
    response = requests.post(url=api_url, auth=TimeTapAuthentication(self.key, self.secret), params=params)
    return response


def api_delete_request(self, url, params: dict = {}):
    api_url = self.base_url + url
    response = requests.delete(url=api_url, auth=TimeTapAuthentication(self.key, self.secret), params=params)
    return response


def api_patch_request(self, url, params: dict = {}):
    api_url = self.base_url + url
    response = requests.patch(url=api_url, auth=TimeTapAuthentication(self.key, self.secret), params=params)
    return response


def api_put_request(self, url, params: dict = {}):
    api_url = self.base_url + url
    response = requests.put(url=api_url, auth=TimeTapAuthentication(self.key, self.secret), params=params)
    return response
