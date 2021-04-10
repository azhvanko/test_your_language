from uuid import UUID

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.tests.utils import AccountsMixin
from accounts.models import ActivationLink


class AuthModelsTestCase(AccountsMixin, TestCase):
    """
    Helper base class for all the follow test cases.
    """
    @classmethod
    def setUpTestData(cls):
        cls.new_user = User.objects.create_user(**cls.users['new_user'])


class ActivationLinkTest(AuthModelsTestCase):

    def test_object_creation(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        self.assertIsInstance(activation_link, ActivationLink)
        self.assertEqual(activation_link.user.username, user.username)
        self.assertFalse(activation_link.user.is_active)
        self.assertIsInstance(activation_link.id, UUID)

    def test_name(self):
        activation_link = self.create_activation_link(self.new_user)
        field_label = activation_link._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'Ссылка для активации')

    def test_user(self):
        activation_link = self.create_activation_link(self.new_user)
        fk = activation_link._meta.get_field('user').one_to_one
        self.assertTrue(fk)

    def test_meta(self):
        self.assertEqual(ActivationLink._meta.verbose_name, 'Ссылка для активации')
        self.assertEqual(ActivationLink._meta.verbose_name_plural, 'Ссылки для активации')

    def test_str_method(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        self.assertEqual(str(activation_link), user.username)

    def test_get_absolute_url(self):
        user = self.new_user
        activation_link = self.create_activation_link(user)
        self.assertEqual(
            activation_link.get_absolute_url(),
            f'/accounts/profile/{user.username}/activate/{activation_link.id}/'
        )
