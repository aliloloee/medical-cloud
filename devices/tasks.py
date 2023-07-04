from celery import shared_task
from devices.utils import generate_otp
from hub.redis_conf import HUBCACHE

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string



@shared_task
def send_email_device(*args, **kwargs) :
    # Send activation code
    code      = generate_otp()
    device_id = kwargs.get('device_id', None)
    lang      = kwargs.get('lang', None)
    to        = kwargs.get('to', None)

    HUBCACHE.cache_activation_key(key=device_id, value=code)

    if settings.DEBUG :
        send_mail(
            'Device Activation',
            f'Device id:{device_id}, activation code:{code}, language:{lang}',
            'info@hub.com',
            [to]
        )
        print(code, device_id, lang)

    else :
        text_content = f'Device id:{device_id}, activation code:{code}, language:{lang}'
        html_content = render_to_string("emails/device_activation.html", {"code": code, "id": device_id})
        msg = EmailMultiAlternatives('Device Activation', text_content, 'info@vivexahealth.com', [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


