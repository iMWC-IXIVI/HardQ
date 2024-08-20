from django.db.models import Count, Min
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import Subscription, Balance
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """

    if created:
        data = Group.objects.values_list('group').annotate(Count('group'))

        group_id = sorted(data, key=lambda x: x[-1])[0][0]
        course_id = instance.course.pk
        user_id = instance.user.pk

        Group.objects.create(
            course_id=course_id,
            user_id=user_id,
            group=group_id
        )
