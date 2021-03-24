from uuid import uuid4

from django.contrib.auth.models import User

from accounts.models import ActivationLink


class AccountsMixin:
    app_name = 'accounts'
    default_test_users_password = 'test_password'
    user = {
        'username': 'test_user_0',
        'password': 'test_password',
        'email': 'test_user_0@example.com',
        'is_active': False,
    }

    fixtures = ['users', ]

    @staticmethod
    def create_activation_link(
            username: str,
            password: str,
            email: str,
            is_active: bool
    ) -> ActivationLink:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_active=is_active
        )
        activation_link = ActivationLink(user=user).save()
        return activation_link

    @staticmethod
    def get_fake_uuid4() -> str:
        return str(uuid4())
