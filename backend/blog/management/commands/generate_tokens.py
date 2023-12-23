from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Generate tokens for all existing users."

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()
        num_tokens_created = 0

        for user in users:
            try:
                _, created = Token.objects.get_or_create(user=user)
                if created:
                    num_tokens_created += 1
            except Exception:
                raise CommandError(
                    f"Unable to get or create a token for the user with id {user.pk}"
                )

        info_msg = ""
        if num_tokens_created == 0:
            info_msg = "No new tokens created."
        elif num_tokens_created > 0:
            info_msg = f"{num_tokens_created} new tokens created."

        self.stdout.write(self.style.SUCCESS(info_msg))
