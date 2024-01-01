from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterUserTest(TestCase):
    # Test creating a new user with a super long email. Does the max_length in the
    # serializer provide a different max_length than in the model definiition?
    # E.g., eamil
    pass

class GenerateTokensTest(TestCase):
    def test_command_with_args(self):
        # Test with wrong username.
        out = StringIO()
        call_command("generate_tokens", "--users", "messi", stderr=out)
        self.assertIn("The user(s) passed do not exist.", out.getvalue())
        out.close()

        # Create new users.
        user_1 = User.objects.create_user(username="user_1", password="password1")
        user_2 = User.objects.create_user(username="user_2", password="password2")

        # Test with valid users.
        out = StringIO()
        call_command("generate_tokens", "--users", "user_1", "user_2", stdout=out)
        self.assertIn("No new tokens were created.", out.getvalue())
        out.close()

        # Verify that these users have tokens.
        token = Token.objects.filter(user=user_1).first()
        self.assertIsNotNone(token)
        token = Token.objects.filter(user=user_2).first()
        self.assertIsNotNone(token)

    def test_command_output(self):
        """Verify that the post_save signal was triggered after the users were created and we
        should not have any new tokens created (by the management script) for these new users,
        as they should have been created by the post_save signal."""
        # Create new users.
        user_1 = User.objects.create_user(username="user_1", password="password1")
        user_2 = User.objects.create_user(username="user_2", password="password2")

        out = StringIO()
        call_command("generate_tokens", stdout=out)
        self.assertIn("No new tokens were created.", out.getvalue())

        # Verify that these users have tokens.
        token = Token.objects.filter(user=user_1).first()
        self.assertIsNotNone(token)
        token = Token.objects.filter(user=user_2).first()
        self.assertIsNotNone(token)
