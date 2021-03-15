from typing import Dict, Tuple

from django.test import TestCase
from django.urls import reverse

from language_tests.models import TestResult
from language_tests.tests.utils import LanguageTestMixin


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
            self.number_published_test_types
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
                kwargs={'pk': self.number_published_test_types + 1}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertContains(response, '<title>test_type_1</title>')

    def test_context_data(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertIsNotNone(response.context_data.get('language_test', None))


class LanguageTestViewTest(LanguageTestMixin, TestCase):
    path_name = 'language_test'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tests/1/test/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/language_test.html'
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
                kwargs={'pk': self.number_published_test_types + 1}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_question_list_with_logged_in_user(self):
        user = 'test_user_1'
        login = self.client.login(
            username=user,
            password=self.default_test_users_password
        )
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [i.question_id for i in response.context_data['questions']],
            [i for i in range(11, 11 + self.default_number_test_questions)]
        )

    def test_question_list_with_anonymous_user(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'AnonymousUser')
        self.assertEqual(
            len(response.context_data['questions']),
            self.default_number_test_questions
        )

    def test_context_data(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertIsNotNone(response.context_data.get('language_test', None))
        self.assertIsNotNone(response.context_data.get('questions', None))

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name, kwargs={'pk': 1}))
        self.assertContains(response, '<title>test_type_1</title>')


class LanguageTestResultViewTest(LanguageTestMixin, TestCase):
    path_name = 'test_result'

    def get_answers(self, key: str) -> Tuple[Dict, Dict]:
        user_answers = {
            # all answers correct
            'correct': {
                str(i): 1
                for i in range(1, self.default_number_test_questions + 1)
            },
            # all answers wrong
            'wrong': {
                str(i): 4
                for i in range(1, self.default_number_test_questions + 1)
            },
            # all answers empty
            'empty': {
                str(i): ''
                for i in range(1, self.default_number_test_questions + 1)
            },
        }
        return user_answers[key], user_answers['correct']

    @staticmethod
    def get_user_answers(user: str) -> Dict[str, int]:
        test_result = TestResult.objects.filter(user__username=user).values(
            'question_id',
            'answer_id'
        )
        return {
            str(item['question_id']): item['answer_id']
            for item in test_result
        }

    def test_HTTP404_for_GET_request(self):
        response = self.client.get('/result/')
        self.assertEqual(response.status_code, 404)

    def test_HTTP404_for_GET_request_by_name(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 404)

    def test_empty_POST_request(self):
        response = self.client.post(
            reverse(self.path_name),
            {},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], {})

    def test_list_correct_answers(self):
        for key in ('correct', 'wrong', 'empty'):
            user_answers, correct_answers = self.get_answers(key)
            response = self.client.post(
                reverse(self.path_name),
                user_answers,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['data'], correct_answers)

    def test_do_not_save_user_answer_in_db(self):
        user = 'test_user_2'
        user_answers, _ = self.get_answers('empty')
        login = self.client.login(
            username=user,
            password=self.default_test_users_password
        )
        response = self.client.post(
            reverse(self.path_name),
            user_answers,
            content_type='application/json'
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertEqual({}, self.get_user_answers(user))

    def test_save_user_answer_in_db(self):
        user = 'test_user_2'
        user_answers, _ = self.get_answers('correct')
        login = self.client.login(
            username=user,
            password=self.default_test_users_password
        )
        response = self.client.post(
            reverse(self.path_name),
            user_answers,
            content_type='application/json'
        )
        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], self.get_user_answers(user))
