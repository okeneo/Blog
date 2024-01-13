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

    def test_register_new_user(self):
        # Test creating a new user.
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertIn("detail", response_data)
        self.assertEqual(response_data["detail"], "User registered successfully.")

        # Test that the user instance was created in the database.
        user = User.objects.filter(username="new_user", email="new_user@gmail.com").first()
        self.assertIsNotNone(user)
        self.assertEqual("new_user", user.username)
        self.assertEqual("new_user@gmail.com", user.email)

    def test_register_user_with_existing_username(self):
        # Create a new user.
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password": "@123tza..",
        }
        User.objects.create_user(**data)

        # Test creating a user with an existing username.
        data = {
            "username": "new_user",
            "email": "another_user@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("The username 'new_user' is already registered.", response_data["username"])

    def test_register_user_with_existing_email(self):
        # Create a new user.
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password": "@123tza..",
        }
        User.objects.create_user(**data)

        # Test creating a user with an existing email.
        data = {
            "username": "another_user",
            "email": "new_user@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("email", response_data)
        self.assertIn(
            "The email address 'new_user@gmail.com' is already registered.", response_data["email"]
        )

    def test_register_user_with_existing_username_and_email(self):
        # Create a new user.
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password": "@123tza..",
        }
        User.objects.create_user(**data)

        # Test creating a user with an existing username and email.
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
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
            "The email address 'new_user@gmail.com' is already registered.", response_data["email"]
        )

    def test_register_user_with_invalid_username(self):
        data = {
            "username": "badcharacter!",
            "email": "new_user@gmail.com",
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

    def test_register_user_with_invalid_email(self):
        data = {
            "username": "validusername",
            "email": "new_user",
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

    def test_register_user_with_invalid_passwords(self):
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
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

    def test_register_user_with_non_matching_passwords(self):
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
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

    def test_register_user_with_blank_username(self):
        data = {
            "username": "",
            "email": "new_user@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("This field may not be blank.", response_data["username"])

    def test_register_user_with_blank_email(self):
        data = {
            "username": "new_user",
            "email": "",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("email", response_data)
        self.assertIn("This field may not be blank.", response_data["email"])

    def test_register_user_with_missing_username(self):
        data = {
            "email": "new_user@gmail.com",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("This field is required.", response_data["username"])

    def test_register_user_with_missing_email(self):
        data = {
            "username": "new_user",
            "password1": "@123tza..",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("email", response_data)
        self.assertIn("This field is required.", response_data["email"])

    def test_register_user_with_missing_password1(self):
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password2": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("password1", response_data)
        self.assertIn("This field is required.", response_data["password1"])

    def test_register_user_with_missing_password2(self):
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
            "password1": "@123tza..",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("password2", response_data)
        self.assertIn("This field is required.", response_data["password2"])

    def test_register_user_with_missing_passwords(self):
        data = {
            "username": "new_user",
            "email": "new_user@gmail.com",
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("password1", response_data)
        self.assertIn("password2", response_data)
        self.assertIn("This field is required.", response_data["password1"])
        self.assertIn("This field is required.", response_data["password2"])

    def test_register_user_with_no_data(self):
        data = {}
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn("username", response_data)
        self.assertIn("email", response_data)
        self.assertIn("password1", response_data)
        self.assertIn("password2", response_data)
        self.assertIn("This field is required.", response_data["username"])
        self.assertIn("This field is required.", response_data["email"])
        self.assertIn("This field is required.", response_data["password1"])
        self.assertIn("This field is required.", response_data["password2"])


class LoginUserTest(TestCase):
    def setUp(self):
        self.url = "/blog/login/"
        self.client = Client()

        # Create a new user.
        self.user = User.objects.create_user(
            username="new_user", email="new_user@gmail.com", password="@123tza.."
        )


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
#             "email": "new_user@gmail.com",
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


# class LogoutUserTest(TestCase):
#     def setUp(self):
#         self.url = "/blog/logout/"
#         self.client = Client()


# class UserProfileTest(TestCase):
#     def setUp(self):
#         self.url = "/blog/"
#         self.client = Client()

# Test retrieving a user profile with different token and username combinations.
