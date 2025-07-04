import os
import yaml

class Confg:
    def __init__(self):
        self.data = self._load_config()
        env = self.data["env"]
        env_config = self.data["environments"][env]

        self.BASE_URL_API = env_config["base_url_api"]
        self.TIMEOUT = env_config["timeout"]
        self.HEADERS = env_config["headers"]
        self.AUTH_TOKEN = env_config.get("auth_token", None)


    def _load_config(self):
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(path, "r") as f:
            return yaml.safe_load(f)