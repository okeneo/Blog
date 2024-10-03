from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    body = models.TextField()
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
