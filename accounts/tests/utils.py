from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from pytz import timezone

from accounts.models import ActivationLink
from test_your_language.settings import TIME_ZONE


class AccountsMixin:
    app_name = 'accounts'
    default_test_users_password = 'test_password'
    users = {
        'active_user': {
            'username': 'test_user_1',
            'password': default_test_users_password,
            'email': 'test_user_1@example.com',
            'is_active': True,
            'last_login': datetime.now(timezone(TIME_ZONE)) + timedelta(days=1)
        },
        'deactivated_user': {
            'username': 'test_user_2',
            'password': default_test_users_password,
            'email': 'test_user_2@example.com',
            'is_active': False,
            'last_login': datetime.now(timezone(TIME_ZONE)) + timedelta(days=1)
        },
        'new_user': {
            'username': 'test_user_3',
            'password': default_test_users_password,
            'email': 'test_user_3@example.com',
            'is_active': False,
            'last_login': None
        },
    }

    @staticmethod
    def create_activation_link(user: User) -> ActivationLink:
        activation_link = ActivationLink.objects.create(user=user)
        activation_link.save()
        return activation_link

    @staticmethod
    def get_fake_uuid4() -> str:
        return str(uuid4())
