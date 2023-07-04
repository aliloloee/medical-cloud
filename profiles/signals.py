from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
# from django.utils.translation import get_language

from profiles.models import Profile, CustomProfile
from profiles.utils import ProfileType
# from profiles.tasks import send_email_custom_profile


@receiver(post_save, sender=get_user_model())
def post_create_profile(sender, instance, created, **kwargs) :
    """
    Create Profile instance for new users. Superusers will have free type profiles.
    """
    if created :
        profile = Profile.objects.using(instance._state.db).create(user=instance)

    if instance.is_superuser :
        profile, _ = Profile.objects.using(instance._state.db).get_or_create(user=instance)
        profile.type = ProfileType.FREE
        profile.save()

@receiver(post_save, sender=get_user_model())
def post_create_custom_profile(sender, instance, created, **kwargs) :
    """
    Create Custom Profile instance for new users.
    """
    if created :
        custom_profile = CustomProfile.objects.using(instance._state.db).create(user=instance)

        #? This email is sent before account activation email. it should be after
        #? Also such email is better to be sent after user's account is activated not when user's account is still inactive
        #** For better performance, this email is sent in accounts.serializer.VerifySerializer where user account is activated
        # send_email_custom_profile.apply_async(kwargs={
        #                                 'lang': get_language(),
        #                                 'to': instance.email,
        #                                 'firstname': instance.firstname,
        #                                 'lastname': instance.lastname,
        #                                 })


