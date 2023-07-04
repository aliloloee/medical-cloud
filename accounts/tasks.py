from celery import shared_task

from django.core.management import call_command
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

@shared_task
def clear_expired_blacklisted_tokens(*args, **kwargs) :
    call_command('flushexpiredtokens')

    #* The peroidic tasks work fine now even with Asia/Tehran timezone, but maybe for more repeatations of
    #* these periodic task, a need for reseting the database scheduler appears. 
    #* This is the link related to this issue if it occures :
    # https://django-celery-beat.readthedocs.io/en/latest/index.html#:~:text=Important%20Warning%20about%20Time%20Zones

    print('Expired blacklisted tokens were dropped from the database.')


@shared_task
def send_email(*args, **kwargs) :
    # Send activation link
    token  = kwargs.get('token', None)
    hub_id = kwargs.get('hub_id', None)
    lang   = kwargs.get('lang', None)
    to     = kwargs.get('to', None)
    activation = kwargs.get('activation', None)
    reset  = kwargs.get('reset', None)

    if activation :

        if settings.DEBUG :
            send_mail(
                'Account Activation',
                f'id:{hub_id}, activation code:{token}, language:{lang}',
                'info@hub.com',
                [to]
            )
            print(token, hub_id, lang)

        else :
            text_content = f'Hub id:{hub_id}, activation token:{token}, language:{lang}'
            html_content = render_to_string("emails/account_activation.html", {"code": token, "id": hub_id})
            msg = EmailMultiAlternatives('Account Activation', text_content, 'info@vivexahealth.com', [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    
    elif reset :

        if settings.DEBUG :
            send_mail(
                'Password reset',
                f'id:{hub_id}, reset code:{token}, language:{lang}',
                'info@hub.com',
                [to]
            )
            print(token, hub_id, lang)

        else :
            text_content = f'Hub id:{hub_id}, reset token:{token}, language:{lang}'
            html_content = render_to_string("emails/password_reset.html", {"code": token, "id": hub_id})
            msg = EmailMultiAlternatives('Password reset', text_content, 'info@vivexahealth.com', [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

