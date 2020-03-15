
from django.test import TestCase, Client

from django.urls import reverse

class CoreViewTests(TestCase):

    def test_homepage(self):
        """test the index route"""
        client = Client()
        response = client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="core/index.html", msg_prefix="")

    def test_elements(self):
        """test the elements route"""
        client = Client()
        response = client.get(reverse("elements"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name="core/elements.html", msg_prefix="")