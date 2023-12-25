from account.models import UserProfile
from django.db import models
from django.db.models.signals import pre_save
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

    author = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    class Meta:
        ordering = ["-publish_date"]

    def __str__(self):
        return self.title


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(receiver=pre_save_blog_post_receiver, sender=Post)
