from django.db.models import signals

from django.contrib.auth import get_user_model
from users.models import UserProfile


User = get_user_model()


def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


signals.post_save.connect(create_profile, sender=User)