from celery import shared_task

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string



@shared_task
def send_email_custom_profile(*args, **kwargs) :
    # Send activation code
    lang        = kwargs.get('lang', None)
    to          = kwargs.get('to', None)
    firstname   = kwargs.get('firstname', None)
    lastname    = kwargs.get('lastname', None)


    if settings.DEBUG :
        send_mail(
            'Profile Completion',
            f'User:{firstname} {lastname}, language:{lang}',
            'info@hub.com',
            [to]
        )
        print(firstname, lastname, lang)

    else :
        text_content = f'User:{firstname} {lastname}, language:{lang}'
        html_content = render_to_string("emails/profile_completion.html", {"firstname": firstname, "lastname": lastname})
        msg = EmailMultiAlternatives('Profile Completion', text_content, 'info@vivexahealth.com', [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


