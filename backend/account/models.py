from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(AbstractUser):
    """A custom user in the system. This user can be an author, admin or reader."""

    AUTHOR = "AUTHOR"
    ADMIN = "ADMIN"
    READER = "READER"
    ROLE_CHOICES = (
        (AUTHOR, AUTHOR),
        (ADMIN, ADMIN),
        (READER, READER),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=READER)
    bio = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name="email address")

    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class BaseVerificationToken(models.Model):
    """An abstract superclass for verifying a user.

    Each token is deleted once verification completes successfully.

    Additionally, a user will have at most one of each subclassed token associated with their
    account at any given time."""

    key = models.UUIDField(default=uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def is_expired(self, expiry_life):
        expiration_time = self.created_at + timezone.timedelta(seconds=expiry_life)
        return timezone.now() > expiration_time

    def save_unique_token(self, model_class):
        # Check if the generated UUID is not unique (however astronomically unlikely that is)
        # in the database and generate a new unique UUID. Exclude the current instance from
        # this lookup. This is important because each token should point to a unique user.
        while model_class.objects.filter(key=self.key).exclude(id=self.id).exists():
            self.key = uuid4()
            self.created_at = timezone.now()

    def save(self, *args, **kwargs):
        self.save_unique_token(self.__class__)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.key)


class VerificationEmailToken(BaseVerificationToken):
    """This is used for verifying the email address of a new user.

    If a user makes a request to resend a new verification link, the current token is deleted and
    replaced with a new token, carrying over the previous number of send_attempts.

    If the user fails to verify their email within MAX_TIME_TO_CONFIRM_EMAIL amount of time, the
    token is deleted (along with the unverified user)."""

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    send_attempts = models.IntegerField(default=0)

    @property
    def is_expired(self):
        return super().is_expired(settings.VERIFICATION_EMAIL_TOKEN_EXPIRY_LIFE)

    @property
    def has_exceeded_maximum_attempts(self):
        return self.send_attempts >= settings.VERIFICATION_EMAIL_TOKEN_MAX_ATTEMPTS

    def increment_send_attempts(self):
        """Increment the number of times we have tried to send the user a verification email."""
        self.send_attempts += 1
        self.save(update_fields=["send_attempts"])


class VerificationEmailUpdateToken(BaseVerificationToken):
    """This is used for verifiying a user's updated email address."""

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    new_email = models.EmailField(max_length=255, unique=True, verbose_name="new email address")

    @property
    def is_expired(self):
        return super().is_expired(settings.VERIFICATION_EMAIL_UPDATE_TOKEN_EXPIRY_LIFE)


class VerificationResetPasswordToken(BaseVerificationToken):
    """This is used to allow a user to reset their password."""

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    @property
    def is_expired(self):
        return super().is_expired(settings.VERIFICATION_RESET_PASSWORD_TOKEN_EXPIRY_LIFE)


@receiver(pre_delete, sender=UserProfile)
def change_blog_post_and_comment_author(sender, instance=None, created=False, **kwargs):
    """Before a user is deleted, check if they are associated with any posts, comments or reactions.
    If they are, update the user under these objects to a new user before deleting them. This is to
    prevent a cascading deletion of these objects or protection of the user."""
    from post.models import Comment, Post, Reaction

    deleted_user = UserProfile.objects.get(username="deleted_user")

    if instance.posts.exists():
        Post.objects.filter(author=instance).update(author=deleted_user)

    if instance.comments.exists():
        Comment.objects.filter(user=instance).update(user=deleted_user)

    if instance.reactions.exists():
        Reaction.objects.filter(user=instance).update(user=deleted_user)
