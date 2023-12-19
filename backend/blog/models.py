from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models


class ProfileUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifier for authentication
    instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set.")
        if not password:
            raise ValueError("The password field must be set.")

        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class ProfileUser(AbstractUser, PermissionsMixin):
    """Custom user in the system. This user can be an author, admin or reader."""

    AUTHOR = "AUTHOR"
    ADMIN = "ADMIN"
    READER = "READER"
    ROLE_CHOICES = (
        (AUTHOR, AUTHOR),
        (ADMIN, ADMIN),
        (READER, READER),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default=READER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ProfileUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.role not in dict(self.ROLE_CHOICES).keys():
            raise ValidationError("Invalid role.")

        group_name = self.get_role_display()
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            if self.role == self.AUTHOR:
                group.permissions.add(
                    Permission.objects.get(codename="can_create_post"),
                    Permission.objects.get(codename="can_update_post"),
                    Permission.objects.get(codename="can_delete_post"),
                    Permission.objects.get(codename="can_publish_post"),
                )
            elif self.role == self.ADMIN:
                group.permissions.add(
                    Permission.objects.get(codename="can_update_post"),
                    Permission.objects.get(codename="can_delete_post"),
                    Permission.objects.get(codename="can_publish_post"),
                )


class Profile(models.Model):
    """Contains information about a user in the system, that will be displayed on the blog site."""

    bio = models.CharField(max_length=240, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.user.get_username()


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


class Category(models.Model):
    TECHNOLOGY = "Technology"
    LIFE = "Life"
    CATEGORY_CHOICES = (
        (TECHNOLOGY, TECHNOLOGY),
        (LIFE, LIFE),
    )

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)


class Post(models.Model):
    class Meta:
        ordering = ["-publish_date"]

    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(ProfileUser, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category)
