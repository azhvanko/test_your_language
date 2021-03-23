from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import LoginForm, SignUpForm


class SignUpFormTest(TestCase):
    form_fields = {'username', 'email', 'password1', 'password2'}
    fixtures = ['users', ]
    user = {
        'username': 'test_user_0',
        'email': 'test_user_0@example.com',
        'password1': 'ce09wefadkln9af12345678',
        'password2': 'ce09wefadkln9af12345678'
    }

    def test_fields(self):
        form = SignUpForm()
        self.assertEqual(len(form.fields), len(self.form_fields))
        self.assertTrue(all(field in self.form_fields for field in form.fields))

    def test_valid_form(self):
        form = SignUpForm(data=self.user)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        user = dict(self.user)
        user['email'] = 'test_user_1@example.com'
        form = SignUpForm(data=user)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'].get_json_data()[0]['code'],
            'registered_email'
        )
        self.assertEqual(
            form.errors['email'].get_json_data()[0]['message'],
            str(form.error_messages['registered_email'])
        )


class LoginFormTest(TestCase):
    form_fields = {'username', 'password'}
    fixtures = ['users', ]
    user = {
        'username': 'test_user_1',
        'password': 'test_password',
    }

    def test_fields(self):
        form = LoginForm(request=None)
        self.assertEqual(len(form.fields), len(self.form_fields))
        self.assertTrue(all(field in self.form_fields for field in form.fields))

    def test_valid_form(self):
        form = LoginForm(None, self.user)
        self.assertTrue(form.is_valid())

    def test_unconfirmed_email(self):
        user = User.objects.get(username=self.user['username'])
        user.is_active = False
        user.last_login = None
        user.save()
        form = LoginForm(None, self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors().get_json_data()[0]['code'],
            'unconfirmed_email'
        )
        self.assertEqual(
            form.non_field_errors().get_json_data()[0]['message'],
            str(form.error_messages['unconfirmed_email'])
        )
