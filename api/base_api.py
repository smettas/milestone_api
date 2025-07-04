import requests
from config.config import Confg
from utils.logger import get_logger


class BaseAPI:
    def __init__(self):
        cfg = Confg()
        self.logger = get_logger("base_api")
        self.session = requests.Session()
        self.base_url = cfg.BASE_URL_API
        self.hedders = cfg.HEADERS
        self.auth_token = cfg.AUTH_TOKEN

    def get(self, endpoint, headers=None, params=None):
        url = self.base_url + endpoint
        headers = self._add_auth(headers)
        self.logger.info(f"[GET] URL: {url} | PARAMS: {params}")
        response = self.session.get(url, headers=self.hedders, params=params)
        self._log_response(response)
        return response
    
    def post(self, endpoint, headers=None, json=None):
        url = self.base_url + endpoint
        headers = self._add_auth(headers)
        self.logger.info(f"[POST] URL: {url} | JSON: {json}")
        response = self.session.post(url, headers=self.hedders, json=json)
        self._log_response(response)
        return response
    
    def put(self, endpoint, headers=None, json=None):
        url = self.base_url + endpoint
        headers = self._add_auth(headers)
        self.logger.info(f"[PUT] URL: {url} | JSON: {json}")
        response = self.session.put(url, headers=self.hedders, json=json)
        self._log_response(response)
        return response

    def delete(self, endpoint, headers=None):
        url = self.base_url + endpoint
        headers = self._add_auth(headers)
        self.logger.info(f"[DELETE] URL: {url}")
        response = self.session.delete(url, headers=self.hedders)
        self._log_response(response)
        return response
    
    def _add_auth(self, headers):
        if self.auth_token:  #If an auth_token is found in config, this if block will execute or it will skip this block
            headers = headers or {}  #This sets headers = {} (an empty dict) or headers is already passed	Keeps using your passed headers
            headers["Authorization"] = f"Bearer {self.auth_token}"   #✅ This is how most token-based APIs work.
            return headers

    def _log_response(self, response):
        self.logger.info(f"Status code: {response.status_code}")
        try:
            self.logger.debug(f"Response Body: {response.json()}")
        except Exception as e:
            try:
                self.logger.debug(response.content.decode("utf-8", errors="ignore"))
            except:
                self.logger.debug("Non-decodable response body.")