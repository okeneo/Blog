from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = """Generates tokens for users that are passed in as arguments. Generates
    tokens for all existing users if no users are passed in."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            "-u",
            nargs="+",
            type=str,
            dest="usernames",
            help="Usernames to generate tokens for.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        usernames = options["usernames"]
        User = get_user_model()
        if usernames:
            users = User.objects.filter(username__in=usernames)
            if not users:
                self.stderr.write("The user(s) passed do not exist.")
                return
        else:
            users = User.objects.all()

        num_tokens_created = 0
        for user in users:
            _, created = Token.objects.get_or_create(user=user)
            if created:
                num_tokens_created += 1

        info_msg = ""
        if num_tokens_created == 0:
            info_msg = "No new tokens were created."
        elif num_tokens_created > 0:
            info_msg = f"{num_tokens_created} new token(s) created."

        self.stdout.write(info_msg)
