from celery import shared_task

from .models import PhoneToken


@shared_task
def send_sms_verification_code(phone):
    import time

    time.sleep(2)

    PhoneToken.objects.update_or_create(
        phone=phone, defaults={"token": "0000", "is_verified": False}
    )

    return {"status": "success", "phone": phone}
