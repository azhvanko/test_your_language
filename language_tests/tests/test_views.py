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


class LanguageTestDetailViewTest(LanguageTestMixin, TestCase):
    path_name = 'language_test_preview'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tests/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/language_test_preview.html'
        )

    def test_HTTP404_for_invalid_test_type(self):
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'pk': self.number_all_test_types + 1}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_HTTP404_for_not_published_test_type(self):
        response = self.client.get(
            reverse(
                self.path_name,
                kwargs={'pk': self.number_active_test_types + 1}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertContains(response, '<title>test_type_1</title>')

    def test_context_data(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertIsNotNone(response.context_data.get('language_test', None))
