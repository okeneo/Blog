from account.controller import get_sentinel_user
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Tag(models.Model):
    SOFTWARE_ENGINNERING = "Software Engineering"
    DJANGO = "Django"
    GRIT = "Grit"
    TAG_CHOICES = (
        (SOFTWARE_ENGINNERING, SOFTWARE_ENGINNERING),
        (DJANGO, DJANGO),
        (GRIT, GRIT),
    )

    name = models.CharField(max_length=20, choices=TAG_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    TECHNOLOGY = "Technology"
    LIFE = "Life"
    CATEGORY_CHOICES = (
        (TECHNOLOGY, TECHNOLOGY),
        (LIFE, LIFE),
    )

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # This field indicates whether the user has chosen to delete the comment. Comments that
    # have children comments will not be truly deleted (if deleted by the API endpoint) to
    # preserve the tree structure. The "text" field will instead be cleared and a sentinel
    # user will be used as the new user.
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.text

    def get_like_count(self):
        return self.reactions.filter(reaction_type=Reaction.LIKE).count()

    def get_dislike_count(self):
        return self.reactions.filter(reaction_type=Reaction.DISLIKE).count()

    def user_reaction(self, user):
        try:
            return self.reactions.get(user=user).reaction_type
        except Reaction.DoesNotExist:
            return None

    def soft_delete(self):
        self.is_deleted = True
        self.text = ""
        self.user = get_sentinel_user()
        self.save()

    @classmethod
    def handle_deleted_user_comments(cls, user):
        all_user_comments = cls.objects.filter(user=user)
        leaf_comments = all_user_comments.filter(replies__isnull=True)
        leaf_comments.delete()
        parent_comments = all_user_comments.filter(replies__isnull=False)
        # Soft delete parent comments.
        parent_comments.update(is_deleted=True, text="", user=get_sentinel_user())


class Reaction(models.Model):
    NEUTRAL = "NEUTRAL"
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"
    REACTION_CHOICES = (
        (NEUTRAL, NEUTRAL),
        (LIKE, LIKE),
        (DISLIKE, DISLIKE),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=7, choices=REACTION_CHOICES, default=NEUTRAL)

    class Meta:
        unique_together = ["user", "comment"]

    @classmethod
    def set_reaction(cls, user, comment, reaction_type):
        # Update or create a new reaction for the user and comment.
        cls.objects.update_or_create(
            user=user,
            comment=comment,
            defaults={
                "reaction_type": reaction_type,
            },
        )


@receiver(pre_save, sender=Post)
def create_post_slug(sender, instance=None, created=False, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
