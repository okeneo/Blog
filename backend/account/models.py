from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """This relates to the User model and includes additional information about the user."""

    AUTHOR = "AUTHOR"
    ADMIN = "ADMIN"
    READER = "READER"
    ROLE_CHOICES = (
        (AUTHOR, AUTHOR),
        (ADMIN, ADMIN),
        (READER, READER),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=READER)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        return
    if instance.profile:
        instance.profile.save()
