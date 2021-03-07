from django.test import TestCase
from django.urls import reverse


class LanguageTestMixin:
    app_name = 'language_tests'
    number_active_test_types = 5
    number_all_test_types = 10

    fixtures = [
        'language_test_types',
        'answers',
    ]


class LanguageTestListViewTest(LanguageTestMixin, TestCase):
    path_name = 'language_tests'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tests/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/language_tests.html'
        )

    def test_active_language_test_type_list(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context_data['language_test_list']),
            self.number_active_test_types
        )

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name))
        self.assertContains(response, '<title>Список тестов</title>')
