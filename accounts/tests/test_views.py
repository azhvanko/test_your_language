from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.tests.utils import AccountsMixin
from accounts.models import ActivationLink
from test_your_language.settings import LOGIN_REDIRECT_URL


class AuthViewsTestCase(AccountsMixin, TestCase):
    """
    Helper base class for all the follow test cases.
    """
    unregistered_user = {
        'username': 'test_user_0',
        'email': 'test_user_0@example.com',
    }

    @classmethod
    def setUpTestData(cls):
        cls.active_user = User.objects.create_user(**cls.users['active_user'])
        cls.deactivated_user = User.objects.create_user(**cls.users['deactivated_user'])
        cls.new_user = User.objects.create_user(**cls.users['new_user'])

        assert not User.objects.filter(username=cls.unregistered_user['username'])
        assert not User.objects.filter(email=cls.unregistered_user['email'])


class ActivateUserViewTest(AuthViewsTestCase):
    path_name = 'activate_user'

    def test_view_url_exists_at_desired_location(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        response = self.client.get(
            f'/accounts/profile/{user.username}/activate/{activation_link.pk}/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.context_data)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'user': user.username, 'link': activation_link.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.context_data)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/activate_user.html'
        )

    def test_response_if_user_is_active(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'user': user.username, 'link': self.get_fake_uuid4()}
            )
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['message'],
            'Ваша учётная запись была активирована ранее.'
        )

    def test_response_if_fake_user_and_uuid(self):
        username = self.unregistered_user['username']
        login = self.client.login(
            username=username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'user': username, 'link': self.get_fake_uuid4()}
            )
        )
        self.assertFalse(login)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data['message'],
            (
                'При активации вашей учётной записи произошла ошибка. '
                'Пожалуйста, попробуйте позднее.'
            )
        )

    def test_response_if_fake_user_and_invalid_uuid(self):
        username = self.unregistered_user['username']
        login = self.client.login(
            username=username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            f'/accounts/profile/{username}/activate/{self.get_fake_uuid4()[:-1]}/'
        )
        self.assertFalse(login)
        self.assertEqual(response.status_code, 404)

    def test_response_if_new_user(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'user': user.username, 'link': activation_link.pk}
            )
        )
        activation_links = ActivationLink.objects.filter(
            user__username=user.username
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(activation_links), 0)
        self.assertEqual(
            response.context_data['message'],
            'Ваша учётная запись была успешно активирована.'
        )

    def test_title_value(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'user': user.username, 'link': activation_link.pk}
            )
        )
        self.assertContains(response, '<title>Активация аккаунта</title>')


class DeactivateUserViewTest(AuthViewsTestCase):
    path_name = 'deactivate_user'

    def test_view_url_exists_at_desired_location(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            f'/accounts/profile/{user.username}/deactivate/'
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context_data)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': user.username})
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/deactivate_user.html'
        )
        self.assertIn('form', response.context_data)

    def test_redirect_with_unauthenticated_user(self):
        username = self.unregistered_user['username']
        login = self.client.login(
            username=username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': username})
        )
        self.assertFalse(login)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/accounts/profile/{username}/deactivate/'
        )

    def test_success_redirect_with_authentication_user(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.post(
            reverse(self.path_name, kwargs={'user': user.username}),
            data={
                'username': user.username,
                'password': self.default_test_users_password,
                'next': '/',
            }
        )
        self.assertTrue(login)
        self.assertRedirects(response, reverse('home'))

    def test_title_value(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            f'/accounts/profile/{user.username}/deactivate/'
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Деактивация аккаунта</title>')


class LoginViewTest(AuthViewsTestCase):
    path_name = 'login'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/login.html'
        )

    def test_login_fail_with_new_unactivated_user(self):
        user = self.new_user
        response = self.client.post(
            reverse(self.path_name),
            data={
                'username': user.username,
                'password': self.default_test_users_password
            }
        )
        form = response.context_data['form']
        error = form.non_field_errors().get_json_data()[0]
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertEqual(error['code'], 'unconfirmed_email')

    def test_login_fail_with_deactivated_user(self):
        user = self.deactivated_user
        response = self.client.post(
            reverse(self.path_name),
            data={
                'username': user.username,
                'password': self.default_test_users_password
            }
        )
        self.assertRedirects(
            response,
            reverse('reactivate_user', kwargs={'user': user.username}),
            fetch_redirect_response=False
        )

    def test_login_success_with_activated_user(self):
        user = self.active_user
        response = self.client.post(
            reverse(self.path_name),
            data={
                'username': user.username,
                'password': self.default_test_users_password
            }
        )
        self.assertRedirects(response, LOGIN_REDIRECT_URL)

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name))
        self.assertContains(response, '<title>Авторизация</title>')


class LogoutViewTest(AuthViewsTestCase):
    path_name = 'logout'

    def test_logout_with_all_users_type(self):
        users = {value['username']: True for _, value in self.users.items()}
        users.update({self.unregistered_user['username']: False})
        for username, login_flag in users.items():
            login = self.client.login(
                username=username,
                password=self.default_test_users_password
            )
            response = self.client.get(reverse(self.path_name))
            self.assertEqual(login, login_flag)
            self.assertRedirects(response, reverse('home'))


class ReactivateUserViewTest(AuthViewsTestCase):
    path_name = 'reactivate_user'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/profile/user/reactivate/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': 'user', })
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/reactivate_user.html'
        )

    def test_redirect_if_user_is_authenticate(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': user.username, },)
        )
        self.assertTrue(login)
        self.assertRedirects(response, reverse('home'))

    def test_title_value(self):
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': 'user', })
        )
        self.assertContains(response, '<title>Активация аккаунта</title>')


class SignUpViewTest(AuthViewsTestCase):
    path_name = 'signup'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/sign_up.html'
        )

    def test_signup_fail_if_duplicate_email(self):
        user = self.active_user
        response = self.client.post(
            reverse(self.path_name),
            data={
                'username': self.unregistered_user['username'],
                'email': user.email,
                'password1': self.default_test_users_password,
                'password2': self.default_test_users_password,
            }
        )
        form = response.context_data['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.as_json())
        self.assertEqual(
            'registered_email',
            form.errors['email'].get_json_data()[0]['code'],
        )

    def test_save_new_user_in_db(self):
        response = self.client.post(
            reverse(self.path_name),
            data={
                'username': self.unregistered_user['username'],
                'email': self.unregistered_user['email'],
                'password1': self.default_test_users_password,
                'password2': self.default_test_users_password,
            }
        )
        user = User.objects.get(username=self.unregistered_user['username'])
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(user.is_active)

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name))
        self.assertContains(response, '<title>Регистрация</title>')


class UserProfileViewTest(AuthViewsTestCase):
    path_name = 'profile'

    def test_view_url_exists_at_desired_location(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(f'/accounts/profile/{user.username}/')
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': user.username})
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/profile.html'
        )

    def test_redirect_if_user_is_not_login(self):
        user = self.active_user
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': user.username})
        )
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/accounts/profile/{user.username}/'
        )

    def test_redirect_if_user_uses_invalid_username(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'user': self.unregistered_user['username']}
            )
        )
        self.assertTrue(login)
        self.assertRedirects(
            response,
            reverse(self.path_name, kwargs={'user': user.username})
        )

    def test_title_value(self):
        user = self.active_user
        login = self.client.login(
            username=user.username,
            password=self.default_test_users_password
        )
        response = self.client.get(
            reverse(self.path_name, kwargs={'user': user.username})
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<title>Профиль</title>')
