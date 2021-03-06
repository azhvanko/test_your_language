from django.test import TestCase

from language_tests.models import Answer, LanguageTestType


class LanguageTestTypeTest(TestCase):
    fixtures = ['language_test_types', ]

    @staticmethod
    def create_language_test_type(name: str) -> LanguageTestType:
        return LanguageTestType.objects.create(name=name)

    def test_object_creation(self):
        language_test_type = self.create_language_test_type('test_type_0')
        self.assertEqual(language_test_type.name, 'test_type_0')
        self.assertTrue(language_test_type.is_published)

    def test_objects_creation(self):
        all_test_types = LanguageTestType.objects.all()
        published_test_types = LanguageTestType.objects.filter(is_published=True)
        self.assertEqual(len(all_test_types), 10)
        self.assertEqual(len(published_test_types), 5)

    def test_name_label(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        field_label = language_test_type._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Тип теста')

    def test_name_max_length(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        max_length = language_test_type._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)

    def test_name_unique(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        unique = language_test_type._meta.get_field('name').unique
        self.assertTrue(unique)

    def test_str_method(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        self.assertEqual(str(language_test_type), 'test_type_1')

    def test_get_absolute_url(self):
        language_test_type = LanguageTestType.objects.get(id=1)
        self.assertEqual(language_test_type.get_absolute_url(), '/tests/1/')


class AnswerTest(TestCase):
    fixtures = ['answers', ]

    @staticmethod
    def create_answer(answer: str) -> Answer:
        return Answer.objects.create(answer=answer)

    def test_object_creation(self):
        answer = self.create_answer('answer_0')
        self.assertEqual(answer.answer, 'answer_0')

    def test_objects_creation(self):
        all_answers = Answer.objects.all()
        self.assertEqual(len(all_answers), 40)

    def test_answer_label(self):
        answer = Answer.objects.get(id=1)
        field_label = answer._meta.get_field('answer').verbose_name
        self.assertEqual(field_label, 'Ответ')

    def test_answer_max_length(self):
        answer = Answer.objects.get(id=1)
        max_length = answer._meta.get_field('answer').max_length
        self.assertEqual(max_length, 64)

    def test_answer_unique(self):
        answer = Answer.objects.get(id=1)
        unique = answer._meta.get_field('answer').verbose_name
        self.assertTrue(unique)

    def test_str_method(self):
        answer = Answer.objects.get(id=1)
        self.assertEqual(str(answer), 'answer_1')
