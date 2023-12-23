from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

User = get_user_model()


class GenerateTokensTest(TestCase):
    def setUp(self):
        # Create test users.
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_command_output(self):
        out = StringIO()
        call_command("generate_tokens", stdout=out)
        self.assertIn("2 new tokens created.", out.getvalue())
        call_command("generate_tokens", stdout=out)
        self.assertIn("No new tokens created.", out.getvalue())
