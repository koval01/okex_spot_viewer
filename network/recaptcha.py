import logging
import os

from requests import post as http_post


class Recaptcha:
    def __init__(self, token: str) -> None:
        self.token = token
        try:
            self.private_key = os.getenv("PRIVATE_KEY_RECAPTCHA")
        except Exception as e:
            logging.error("Debug mode %s: %s" % (Recaptcha.__name__, e))

    def check_token(self) -> bool:
        u = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': self.private_key,
            'response': self.token,
        }
        try:
            resp = http_post(u, data=data)
            if resp.status_code >= 200 < 400:
                return resp.json()["success"]
        except Exception as e:
            logging.error("%s error: %s" % (Recaptcha.__name__, e))
        return False
