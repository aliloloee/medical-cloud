from django.dispatch import receiver
from django.db.models.signals import pre_save

from pills.models import PillAlarm

from django_celery_beat.models import PeriodicTask, IntervalSchedule

import json



@receiver(pre_save, sender=PillAlarm)
def ff(sender, instance, **kwargs):
    """
    This signal is created for sending notification to PillAlarm objects which are activated. So, the code below checks to see if the field "is_active" has been set to "True". If yes, then the mechanism of sending notification starts.

    #*The mechanism of sending notification is actually a periodic task. This periodic task .........

    #* Remaining jobs : 1- create a suitable crontab or interval, 2- save the periodic task pk , 3- delete periodic task pk in case a pillalarm is deactivated
    """
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        #* "When creating a PillAlarm instance, the user first creates it then activates"
        # Object is new and has no pk yet
        return

    if not obj.is_active == instance.is_active:
        if obj.is_active == False :  # instance.is_active == True, means alarm is activated
            print('Alarm activated')

            schedule, created = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.SECONDS,
            )

            name = f'send pill notification for alram-id of {obj.pk}'
            try :
                periodic_task = PeriodicTask.objects.create(
                    interval=schedule,
                    name=name,          # description
                    task='pills.tasks.send_pill_notification',
                    kwargs=json.dumps({
                        'pill': obj.pill.name,
                        'alarm-id' : str(obj.pk),
                        'user': obj.user.firstname
                    }),
                )
            except :
                periodic_task = PeriodicTask.objects.get(name=name)

            print(periodic_task.pk)


        elif obj.is_active == True : # instance.is_active == False, means alarm is deactivated
            print('Alarm dectivated')

