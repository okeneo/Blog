import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from .models import Category, Tag

User = get_user_model()


class CreatePost(TestCase):
    def setUp(self):
        self.url = "/blog/post/"
        self.client = Client()

        # Create a new user.
        self.user = User.objects.create_user(
            username="new_user", email="new_user@gmail.com", password="@123tza.."
        )

        # Create a new post.

        # Create categories.
        self.categories_1 = Category.objects.create(name="Life")
        self.categories_1 = Category.objects.create(name="Technology")

        # Create tags.
        self.tag_1 = Tag.objects.create(name="Software Engineering")
        self.tag_2 = Tag.objects.create(name="Django")
        self.tag_3 = Tag.objects.create(name="Grit")

    def test_create_post_without_logging_in(self):
        data = {
            "title": "Test Post",
            "body": "Contrary to popular belief, Lorem Ipsum is not simply "
            "random text. It has roots in a piece of classical Latin literature "
            "from 45 BC.",
            "author": self.user.pk,
            "category": self.categories_1.pk,
            "tag": [self.tag_1.pk, self.tag_2.pk],
        }
        json_data = json.dumps(data)
        response = self.client.post(self.url, data=json_data, content_type="application/json")

        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content)
        self.assertIn("detail", response_data)
        self.assertEqual(response_data["detail"], "Authentication credentials were not provided.")

    def test_create_post_with_authorized_user(self):
        id = self.user.pk
        data = {
            "title": "Test Post",
            "body": "Contrary to popular belief, Lorem Ipsum is not simply "
            "random text. It has roots in a piece of classical Latin literature "
            "from 45 BC",
            "author": id,
            "category": "1",
            "tag": ["1", "2"],
        }
        json_data = json.dumps(data)

        # Add JWT token to request.

        response = self.client.post(self.url, data=json_data, content_type="application/json")

        # self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.content)
        response_data
        # print(response_data)

    def test_get_all_posts(self):
        response = self.client.get(self.url)
        print(response.__dict__)

        # Create a new post.

    def test_get_specific_post(self):
        pass
