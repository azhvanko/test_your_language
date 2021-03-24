from uuid import UUID

from django.test import TestCase

from accounts.tests.utils import AccountsMixin
from accounts.models import ActivationLink


class ActivationLinkTest(AccountsMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.create_activation_link(**cls.user)

    def test_object_creation(self):
        username = self.user['username']
        activation_link = ActivationLink.objects.get(user__username=username)
        self.assertIsInstance(activation_link, ActivationLink)
        self.assertEqual(activation_link.user.username, username)
        self.assertFalse(activation_link.user.is_active)
        self.assertIsInstance(activation_link.id, UUID)

    def test_name(self):
        activation_link = ActivationLink.objects.get(
            user__username=self.user['username']
        )
        field_label = activation_link._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'Ссылка для активации')

    def test_user(self):
        activation_link = ActivationLink.objects.get(
            user__username=self.user['username']
        )
        fk = activation_link._meta.get_field('user').one_to_one
        self.assertTrue(fk)

    def test_meta(self):
        self.assertEqual(ActivationLink._meta.verbose_name, 'Ссылка для активации')
        self.assertEqual(ActivationLink._meta.verbose_name_plural, 'Ссылки для активации')

    def test_str_method(self):
        username = self.user['username']
        activation_link = ActivationLink.objects.get(user__username=username)
        self.assertEqual(str(activation_link), username)

    def test_get_absolute_url(self):
        username = self.user['username']
        activation_link = ActivationLink.objects.get(user__username=username)
        self.assertEqual(
            activation_link.get_absolute_url(),
            f'/accounts/profile/{username}/activate/{activation_link.id}/'
        )
