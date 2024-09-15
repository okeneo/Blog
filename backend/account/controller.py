from django.contrib.auth.models import User


def get_sentinel_user():
    return User.objects.get(username="deleted")


def handle_deleted_user_comments(user):
    leaf_comments = user.comments.filter(parent_comment__isnull=False)
    leaf_comments.delete()
    parent_comments = user.comments.filter(parent_comment__isnull=True)
    parent_comments.update(user=get_sentinel_user(), is_deleted=True, text="")
