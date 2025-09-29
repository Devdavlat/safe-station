import json
import requests
from django.conf import settings


def get_sms_service_token():
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {"email": settings.SMS_SERVICE_EMAIL, "password": settings.SMS_SERVICE_PASSWORD}
    response = requests.request("POST", url, headers={}, data=payload, files=[])
    if response.status_code == 200:
        return json.loads(response.text)["data"].get("token")
