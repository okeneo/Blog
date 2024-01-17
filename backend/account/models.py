from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class UserProfile(AbstractUser):
    """Custom user in the system. This user can be an author, admin or reader."""

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

    def __str__(self):
        return self.username


@receiver(pre_delete, sender=UserProfile)
def change_blog_post_and_comment_author(sender, instance=None, created=False, **kwargs):
    """Before a user is deleted, check if they are associated with any posts, comments or reactions.
    If they are, update the user under these objects to a new user before deleting them."""
    from post.models import Comment, Post, Reaction

    deleted_user = UserProfile.objects.get(username="deleted_user")

    if instance.posts.exists():
        Post.objects.filter(author=instance).update(author=deleted_user)

    if instance.comments.exists():
        Comment.objects.filter(user=instance).update(user=deleted_user)

    if instance.reactions.exists():
        Reaction.objects.filter(user=instance).update(user=deleted_user)
