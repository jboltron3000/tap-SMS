import requests
import re
import pdb
from requests.auth import HTTPBasicAuth
from singer import metrics
import backoff
from datetime import datetime, timedelta
import time
import json 
import xmltodict


def convert(xml_file, xml_attribs=True):
    xml_file = xml_file.decode("utf-8", "replace")
    d = xmltodict.parse(xml_file)
    return json.dumps(d)

def _join(a, b):
    return a.rstrip("/") + b.lstrip("/")

TIME_BETWEEN_REQUESTS = timedelta(microseconds=10)

class Client(object):
    def __init__(self, config):
        self.user_agent = config.get("username")
        self.base_url = ""
        self.auth = HTTPBasicAuth(config["username"], config["password"])
        self.session = requests.Session()
        self.next_request_at = datetime.now()
		
    def prepare_and_send(self, request):
        if self.user_agent:
            request.headers["User-Agent"] = self.user_agent
        return self.session.send(request.prepare())

    def url(self, path, base_url):
        return _join(base_url, path)

    def create_get_request(self, path, **kwargs):
        return requests.Request(method="GET", url=self.url(path), **kwargs)
    
    def _headers(self, headers):
        headers = headers.copy()
        headers["User-Agent"] = self.user_agent
        return headers

    def send(self, method, path, headers={}, **kwargs):
        request = requests.Request(
            method, self.url(path, self.base_url), auth=self.auth,
            headers=self._headers(headers),
            **kwargs
        )
        return self.session.send(request.prepare())

    
    def request(self, tap_stream_id, *args, **kwargs):
        wait = (self.next_request_at - datetime.now()).total_seconds()
        if wait > 0:
            time.sleep(wait)
        with metrics.http_request_timer(tap_stream_id) as timer:
            response = self.send(*args, **kwargs)
            self.next_request_at = datetime.now() + TIME_BETWEEN_REQUESTS
            timer.tags[metrics.Tag.http_status_code] = response.status_code
        if response.status_code == 429:
            raise RateLimitException()
        response.raise_for_status()
        response._content = convert(response._content, True).encode("ascii", "replace")
        return response.json()


