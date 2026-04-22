from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class AnonymousOnlyAuthPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="authuser",
            password="pass12345",
        )

    def test_register_page_redirects_authenticated_users(self):
        self.client.login(username="authuser", password="pass12345")
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:product_list"))

    def test_login_page_redirects_authenticated_users(self):
        self.client.login(username="authuser", password="pass12345")
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("catalog:product_list"))
