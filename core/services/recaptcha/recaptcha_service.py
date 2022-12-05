import os
import requests
import json


class RequestRecaptchaError(Exception):
    pass


class ResponseRecaptchaError(Exception):
    pass


class InvalidRecaptchaError(Exception):
    pass


class RecaptchaService:
    recaptcha_secret_key = os.environ.get('RECAPTCHA_SECRET_KEY', '')

    def __init__(self, response):
        self.response = response

    @staticmethod
    def get_recaptcha_site_key():
        return os.environ.get('RECAPTCHA_SITE_KEY', '')

    def validate_facade(self):
        try:
            self.validate()
        except RequestRecaptchaError as ex:
            return False, str("Error en la peticion")
        except ResponseRecaptchaError:
            return False, str("Problemas con los servicios de google")
        except InvalidRecaptchaError:
            return False, str("Recaptcha no puedo ser validado, consulte con la entidad.")
        except Exception as ex:
            return False, "Error desconocido"

        return True,

    def validate(self):
        try:
            recaptcha_data = {
                "secret": self.recaptcha_secret_key,
                "response": self.response
            }

            response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify?secret={}&response={}'.format(
                    self.recaptcha_secret_key,
                    self.response
                ),
                data=json.dumps(recaptcha_data)
            )
        except Exception as e:
            raise RequestRecaptchaError(e)

        if response.status_code != 200:
            raise ResponseRecaptchaError(response.status_code)

        response_json = response.json()

        if not response_json['success']:
            raise InvalidRecaptchaError()
