import requests
import logging
from datetime import timedelta
from django.conf import settings
from django.utils.crypto import get_random_string

from users.models import User, VerificationCode
from utils.get_object import get_or_none


def send_verification_code(phone_number, verification_type):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    from utils.verification import get_sms_service_token
    code = get_random_string(length=6, allowed_chars="1234567890")
    verification_code, _ = VerificationCode.objects.update_or_create(
        phone_number=phone_number,
        verification_type=verification_type,
        defaults={"code": code, "is_verified": False, "attempts": 0},
    )
    update_expired_at_field(verification_code)

    user = get_or_none(User, phone_number=phone_number)
    verification_code = get_or_none(VerificationCode, phone_number=phone_number, verification_type=verification_type)
    if verification_code:
        if user and not verification_code.user:
            verification_code.user = user
        verification_code.save()
    msg_from = "4546"
    payload = {
        "mobile_phone": phone_number.lstrip("+"),
        "message": text,
        "from": msg_from,
    }
    headers = {"Authorization": f"Bearer {get_sms_service_token()}"}
    print("code: ", code)
    try:
        response = requests.post(url=url, headers=headers, data=payload)
    except Exception as err:
        logging.error(err)
    else:
        return response


def update_expired_at_field(verification_code):
    verification_code.expired_at = verification_code.updated_at + timedelta(minutes=settings.VERIFICATION_CODE_LIFETIME)
    verification_code.save(update_fields=["expired_at"])
