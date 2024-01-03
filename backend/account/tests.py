import json
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterUserTest(TestCase):
    def setUp(self):
        self.url = "/blog/signup/"
        self.client = Client()

    def test_new_user_signup(self):
        # Test creating a new user.
        data = {
            "username": "new_user",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertIn("token", response_data)
        self.assertIsNotNone(response_data["token"])

        # Test that the user instance was created in the database.
        user = User.objects.filter(username="new_user", email="newuser@gmail.com").first()
        self.assertIsNotNone(user)
        self.assertEqual("new_user", user.username)
        self.assertEqual("newuser@gmail.com", user.email)

    def test_duplicate_username_or_email_signup(self):
        # Create a new user.
        data = {
            "username": "new_user",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertIn("token", response_data)
        self.assertIsNotNone(response_data["token"])

        # Test that the user instance was created in the database.
        user = User.objects.filter(username="new_user", email="newuser@gmail.com").first()
        self.assertIsNotNone(user)
        self.assertEqual("new_user", user.username)
        self.assertEqual("newuser@gmail.com", user.email)

        # Test creating a user with the same username.
        data = {
            "username": "new_user",
            "email": "anotheruser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("The username 'new_user' is already registered.", response_data["username"])

        # Test creating a user with the same email.
        data = {
            "username": "another_user",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("email", response_data)
        self.assertIn(
            "The email address 'newuser@gmail.com' is already registered.", response_data["email"]
        )

        # Test creating a user with the same username and email.
        data = {
            "username": "new_user",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("The username 'new_user' is already registered.", response_data["username"])
        self.assertIn("email", response_data)
        self.assertIn(
            "The email address 'newuser@gmail.com' is already registered.", response_data["email"]
        )

        # TODO: Test creating a new user with a super long email. Does the max_length in the
        # serializer email field provide a different max_length than in the model definition?
        # - Testing possible inconsistencies.

    def test_invalid_signup_data(self):
        # Test creating a new user with invalid username.
        data = {
            "username": "",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("This field may not be blank.", response_data["username"])

        # Test creating a new user with another invalid username.
        data = {
            "username": "badcharacter!",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn(
            "Enter a valid username. This value may contain only letters, numbers, and "
            "@/./+/-/_ characters.",
            response_data["username"],
        )

        # Test creating a new user an invalid email.
        data = {
            "username": "validusername",
            "email": "newuser",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("email", response_data)
        self.assertIn(
            "Enter a valid email address.",
            response_data["email"],
        )

        # Test creating a new user an invalid password.
        data = {
            "username": "new_user",
            "email": "newuser@gmail.com",
            "password1": "1",
            "password2": "1",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("password1", response_data)
        self.assertIn(
            "This password is too short. It must contain at least 8 characters.",
            response_data["password1"],
        )
        self.assertIn(
            "This password is too common.",
            response_data["password1"],
        )
        self.assertIn(
            "This password is entirely numeric.",
            response_data["password1"],
        )

        # Test creating a new user when password1 and password2 are not equal.
        data = {
            "username": "new_user",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza...",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("non_field_errors", response_data)
        self.assertIn(
            "Passwords do not match.",
            response_data["non_field_errors"],
        )

    def test_missing_signup_data(self):
        # Missing username, email and passwords.
        pass


class LoginUserTest(TestCase):
    def setUp(self):
        self.url = "/blog/login/"
        self.client = Client()

    def test_login_users(self):
        # Create a new user.
        data = {
            "username": "new_user",
            "email": "newuser@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(
            "/blog/signup/", data=json_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertIn("token", response_data)
        self.assertIsNotNone(response_data["token"])
        signup_token = response_data["token"]

        # Test that the user instance was created in the database.
        user = User.objects.filter(username="new_user", email="newuser@gmail.com").first()
        self.assertIsNotNone(user)
        self.assertEqual("new_user", user.username)
        self.assertEqual("newuser@gmail.com", user.email)

        # Test logging in a user with their username.
        data = {
            "username": "new_user",
            "password": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn("token", response_data)
        self.assertIsNotNone(response_data["token"])
        login_token = response_data["token"]
        self.assertEqual(signup_token, login_token)

        # Test logging in a user that is already logged in.

        # Test logging in without password.

        # Test logging in without username.

        # Test logging in with a user that does not not exist.

        # Test logging in a user with their email.


class LogoutUserTest(TestCase):
    def setUp(self):
        self.url = "/blog/logout/"
        self.client = Client()


class UserProfileTest(TestCase):
    def setUp(self):
        self.url = "/blog/"
        self.client = Client()


class GenerateTokensTest(TestCase):
    def setUp(self):
        # Create new users before each method call.
        self.user_1 = User.objects.create_user(
            username="user_1", email="user_1@gmail.com", password="password1"
        )
        self.user_2 = User.objects.create_user(
            username="user_2", email="user_2@gmail.com", password="password2"
        )

    def test_command_with_args(self):
        # Test with wrong username.
        out = StringIO()
        call_command("generate_tokens", "--users", "messi", stderr=out)
        self.assertIn("The user(s) passed do not exist.", out.getvalue())
        out.close()

        # Test with valid users.
        out = StringIO()
        call_command("generate_tokens", "--users", "user_1", "user_2", stdout=out)
        self.assertIn("No new tokens were created.", out.getvalue())
        out.close()

        # Verify that these users have tokens (that were generated via the post_save signal,
        # not the management script).
        token = Token.objects.filter(user=self.user_1).first()
        self.assertIsNotNone(token)
        token = Token.objects.filter(user=self.user_2).first()
        self.assertIsNotNone(token)

    def test_command_output(self):
        """Verify that the post_save signal was triggered after the users were created and we
        should not have any new tokens created (by the management script) for these new users,
        as they should have been created by the post_save signal."""
        out = StringIO()
        call_command("generate_tokens", stdout=out)
        self.assertIn("No new tokens were created.", out.getvalue())

        # Verify that these users have tokens.
        token = Token.objects.filter(user=self.user_1).first()
        self.assertIsNotNone(token)
        token = Token.objects.filter(user=self.user_2).first()
        self.assertIsNotNone(token)
