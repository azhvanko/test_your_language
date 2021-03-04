from django.db.utils import IntegrityError
from django.test import TestCase

from language_tests.models import LanguageTestType


class LanguageTestTypeTest(TestCase):
    fixtures = ['language_test_types', ]

    @staticmethod
    def create_language_test_type(name: str) -> LanguageTestType:
        return LanguageTestType.objects.create(name=name)

    def test_objects_creation(self):
        all_test_types = LanguageTestType.objects.all()
        published_test_types = LanguageTestType.objects.filter(is_published=True)
        self.assertTrue(len(all_test_types), 10)
        self.assertTrue(len(published_test_types), 5)

    def test_name_label(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        field_label = language_test_type._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Тип теста')

    def test_name_max_length(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        max_length = language_test_type._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            self.create_language_test_type('test_type_1')

    def test_str_method(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        self.assertEqual(str(language_test_type), 'test_type_1')
