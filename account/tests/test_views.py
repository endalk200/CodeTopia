"""Python module for writting tests for views"""
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from django.core import mail

from django.contrib.auth.models import User

from account.views import *
from account.forms import *
from account.urls import *

from django.utils.translation import gettext, gettext_lazy as _


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.user1_cridentials = {
            "username": "test_user_1", 
            "email": "test_email_1@gmail.com", 
            "password": "test_user_1_password"
        }
        self.user2_cridentials = {
            "username": "test_user_2", 
            "email": "test_email_2@gmail.com", 
            "password": "test_user_2_password[]"
        }
        self.user3_cridentials = {
            "username": "test_user_3", 
            "email": "test_email_3@gmail.com", 
            "password": "test_user_3_password[]"
        }

        self.created_user = User.objects.create_user(
            username=self.user1_cridentials["username"], 
            email="test_email_1@gmail.com", 
            password="test_user_1_password")

    def test_CustomLoginView_get(self):
        """test CustomLoginView by requesting page using GET method"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=False)
        response = c.get(reverse("account:user_login"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["title"], "CodeTopia | Login" )
        self.assertIsInstance(response.context["form"], CustomLoginView.form_class)
        self.assertTemplateUsed(response, "account/login.html")

    @override_settings(LOGIN_URL=reverse("homepage"))
    def test_CustomLoginView_post1_valid(self):
        """test CustomLoginView by requesting page using POST method"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=False)
        response = c.post(reverse("account:user_login"),
        {
            "username": self.user1_cridentials["username"],
            "password": self.user1_cridentials["password"]
        })
        self.assertEqual(
            first=response.status_code, 
            second=302, 
            msg="response.status_code Error for http://%s/"% reverse("account:user_login"))
        self.assertRedirects(
            response=response, 
            expected_url=reverse("homepage"), 
            status_code=302, 
            target_status_code=200, 
            msg_prefix='', 
            fetch_redirect_response=True)

    @override_settings(LOGIN_URL=reverse("homepage"))
    def test_CustomLoginView_post2_valid(self):
        """test CustomLoginView by requesting page using POST method"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=False)
        response = c.post(
            reverse("account:user_login"),
            {"username": self.user1_cridentials["username"],
             "password": self.user1_cridentials["password"]},
            follow=True
        )
        # test wether the redirect target status_code is 200
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response=response, 
            expected_url=reverse("homepage"),  # expected redirect target URL
            status_code=302,  # status_code of the first request
            target_status_code=200,  # response.status_code of target view
            msg_prefix='Log in view POST method redirection Error',
            fetch_redirect_response=True)

        self.assertEqual(response.redirect_chain, [(reverse("homepage"), 302)])
        self.assertEqual(
            first=response.context["title"], 
            second="CodeTopia", 
            msg="Redirect target page title Error" )
        self.assertTemplateUsed(response=response, template_name="core/index.html", count=1)

    @override_settings(LOGIN_URL=reverse("homepage"))
    def test_CustomLoginView_post1_invalid(self):
        """test CustomLoginView by requesting page using POST method and invlaid user cridentials"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=False)
        response = c.post(
            reverse("account:user_login"),
            {
                "username": self.user2_cridentials["username"],
                "password": self.user1_cridentials["password"]
            },
            follow=True
        )
        # test wether the redirect target status_code is 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(first=response.context["title"], second="CodeTopia | Login", msg="" )
        self.assertTemplateUsed(response=response, template_name="account/login.html", count=1)


class TestCustomLogoutView(TestCase):
    def setUp(self):
        # user cridenatials to be used for the test
        self.user1_cridentials = {
            "username": "test_user_1", 
            "email": "test_email_1@gmail.com", 
            "password": "test_user_1_password"
        }

        # create user for the Logout test
        self.created_user = User.objects.create_user(
            username=self.user1_cridentials["username"], 
            email="test_email_1@gmail.com", 
            password="test_user_1_password")

    @override_settings(LOGOUT_URL=reverse("homepage"))
    def test_CustomLogoutView_get(self):
        """test CustomLogoutView by requesting view using GET method"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=False)
        # force login to test CustomLogoutView with self.user1_cridentails for self.created_user
        c.force_login(user=self.created_user)
        response = c.get(reverse("account:user_logout"))

        # test wether the response is redirection
        self.assertEqual(
            first=response.status_code, 
            second=302, 
            msg="response.status_code Error for http://%s/ with follow=False"%
                reverse("account:user_logout"))
        self.assertRedirects(
            response=response, 
            expected_url=reverse("homepage"), 
            status_code=302, 
            target_status_code=200, 
            msg_prefix='', 
            fetch_redirect_response=True)

    @override_settings(LOGOUT_URL=reverse("homepage"))
    def test_CustomLogoutView_post(self):
        """test CustomLogoutView by requesting page using POST method"""
        c = Client(HTTP_USER_AGENT='Mozilla/5.0', enforce_csrf_checks=False)
        # force login to test CustomLogoutView with self.user1_cridentails for self.created_user
        c.force_login(user=self.created_user)
        response = c.post(path=reverse("account:user_logout"), follow=True)

        self.assertEqual(
            first=response.status_code, 
            second=200, 
            msg="response.status_code Error for http://%s/ with follow=True"% 
            reverse("account:user_logout"))
        self.assertRedirects(
            response=response, 
            expected_url=reverse("homepage"), 
            status_code=302, 
            target_status_code=200, 
            msg_prefix='', 
            fetch_redirect_response=True)
        self.assertEqual(first=response.context["title"], second="CodeTopia" )
        self.assertTemplateUsed(response=response, template_name="core/index.html", msg_prefix="")
