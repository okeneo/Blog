from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models


class PostPermissions(models.Model):
    PERMISSIONS = {
        "can_create_post": "Can create a new post",
        "can_update_post": "Can update an existing post",
        "can_delete_post": "Can delete a post",
        "can_publish_post": "Can publish a post",
    }

    class Meta:
        managed = False
        permissions = (
            ("can_create_post", "Can create a new post"),
            ("can_update_post", "Can update an existing post"),
            ("can_delete_post", "Can delete a post"),
            ("can_publish_post", "Can publish a post"),
        )


def create_custom_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(PostPermissions)

    for codename, name in PostPermissions.PERMISSIONS.items():
        Permission.objects.create(
            codename=codename,
            name=name,
            content_type=content_type,
        )


# Connect the signal to create permissions when the app is migrated.
models.signals.post_migrate.connect(create_custom_permissions)
