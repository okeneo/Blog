import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()

# TODO: Create users via database API (not register endpoint) except when testing RegisterUserTest.
# Break tests into more functions - They are too long as it stands.
# Isolate tests - A test should not depend on a previous test
# Write a create method for creating users when needed
# Ensure that all tests would otherwise work.
# More: https://chat.openai.com/c/b9fb938d-6d10-4ea5-b0c7-5a5073e46660


class RegisterUserTest(TestCase):
    def setUp(self):
        self.url = "/blog/register/"
        self.client = Client()

    def test_new_user_register(self):
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

    def test_duplicate_username_or_email_register(self):
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

    def test_invalid_register_data(self):
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

        # Test creating a new user with an invalid email.
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

        # Test creating a new user with an invalid password.
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

    def test_missing_register_data(self):
        # Missing username, email and passwords.
        pass


# class LoginUserTest(TestCase):
#     def setUp(self):
#         self.url = "/blog/login/"
#         self.client = Client()

#         # Create a new user.
#         self.user = User.objects.create_user(
#             username="new_user", email="newuser@gmail.com", password="@123tza.."
#         )

#     def test_username_login(self):
#         # Test logging in a user with their username.
#         self.register_token = Token.objects.filter(user=self.user).first().key
#         data = {
#             "username": "new_user",
#             "password": "@123tza..",
#         }
#         json_data = json.dumps(data)
#         response = self.client.post(self.url, data=json_data, content_type="application/json")

#         self.assertEqual(response.status_code, 200)
#         response_data = json.loads(response.content)
#         self.assertIn("token", response_data)
#         self.assertIsNotNone(response_data["token"])
#         login_token = response_data["token"]
#         self.assertEqual(self.register_token, login_token)

#     def test_email_login(self):
#         # Test logging in a user with their email.
#         self.register_token = Token.objects.filter(user=self.user).first().key
#         data = {
#             "email": "newuser@gmail.com",
#             "password": "@123tza..",
#         }
#         json_data = json.dumps(data)
#         response = self.client.post(self.url, data=json_data, content_type="application/json")

#         self.assertEqual(response.status_code, 200)
#         response_data = json.loads(response.content)
#         self.assertIn("token", response_data)
#         self.assertIsNotNone(response_data["token"])
#         login_token = response_data["token"]
#         self.assertEqual(self.register_token, login_token)

#     # def test_login_users(self):
#     #     # Test logging in without password.

#     #     # Test logging with wrong password.

#     #     # Test logging in without username.

#     #     # Test logging in with a user that does not not exist.

#     #     # Test logging in without email.

#     #     # Test logging in with email that does not exist.


class LogoutUserTest(TestCase):
    def setUp(self):
        self.url = "/blog/logout/"
        self.client = Client()


class UserProfileTest(TestCase):
    def setUp(self):
        self.url = "/blog/"
        self.client = Client()

    # Test retrieving a user profile with different token and username combinations.
