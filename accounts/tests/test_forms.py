from django.contrib.auth.models import User
from django.test import TestCase

from accounts.forms import DeactivationForm, LoginForm, SignUpForm
from accounts.tests.utils import AccountsMixin


class AuthFormsTestCase(AccountsMixin, TestCase):
    """
    Helper base class for all the follow test cases.
    """
    @classmethod
    def setUpTestData(cls):
        cls.active_user = User.objects.create_user(**cls.users['active_user'])
        cls.new_user = User.objects.create_user(**cls.users['new_user'])


class DeactivationFormTest(AuthFormsTestCase):
    form_fields = {'username', 'password'}

    def test_fields(self):
        form = DeactivationForm(request=None)
        self.assertEqual(len(form.fields), len(self.form_fields))
        self.assertTrue(all(field in self.form_fields for field in form.fields))

    def test_valid_form(self):
        user = self.users['active_user']
        form = DeactivationForm(None, user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_form_invalid_if_incorrect_password(self):
        user = dict(self.users['active_user'])
        user['password'] = 'fake_password'
        form = DeactivationForm(request=None, data=user)
        password_error = form.errors.get_json_data()['password'][0]
        self.assertFalse(form.is_valid())
        self.assertEqual(password_error['code'], 'invalid_password')
        self.assertEqual(
            password_error['message'],
            str(form.error_messages['invalid_password'])
        )


class LoginFormTest(AuthFormsTestCase):
    form_fields = {'username', 'password'}

    def test_fields(self):
        form = LoginForm(request=None)
        self.assertEqual(len(form.fields), len(self.form_fields))
        self.assertTrue(all(field in self.form_fields for field in form.fields))

    def test_valid_form(self):
        user = self.users['active_user']
        form = LoginForm(None, user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_form_invalid_if_unconfirmed_email(self):
        user = self.users['new_user']
        form = LoginForm(None, user)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors().get_json_data()[0]['code'],
            'unconfirmed_email'
        )
        self.assertEqual(
            form.non_field_errors().get_json_data()[0]['message'],
            str(form.error_messages['unconfirmed_email'])
        )


class SignUpFormTest(AuthFormsTestCase):
    form_fields = {'username', 'email', 'password1', 'password2'}
    unregistered_user = {
        'username': 'test_user_0',
        'email': 'test_user_0@example.com',
        'password1': 'drowssap_resu_tset',
        'password2': 'drowssap_resu_tset'
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        assert not User.objects.filter(username=cls.unregistered_user['username'])
        assert not User.objects.filter(email=cls.unregistered_user['email'])

    def test_fields(self):
        form = SignUpForm()
        self.assertEqual(len(form.fields), len(self.form_fields))
        self.assertTrue(all(field in self.form_fields for field in form.fields))

    def test_valid_form(self):
        form = SignUpForm(data=self.unregistered_user)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_form_invalid_if_registered_email(self):
        user = dict(self.unregistered_user)
        user['email'] = self.active_user.email
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

    def test_form_invalid_if_invalid_username(self):
        user = dict(self.unregistered_user)
        invalid_usernames = ('user.1', 'user!@#$%^&*', 'пользователь',)
        for username in invalid_usernames:
            user['username'] = username
            form = SignUpForm(data=user)
            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors['username'].get_json_data()[0]['code'],
                'invalid_username'
            )
            self.assertEqual(
                form.errors['username'].get_json_data()[0]['message'],
                str(form.error_messages['invalid_username'])
            )
