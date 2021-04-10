from django.test import TestCase
from django.urls import reverse


class HomeViewTest(TestCase):
    app_name = 'home'
    path_name = 'home'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.path_name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            f'{self.app_name}/home.html'
        )

    def test_title_value(self):
        response = self.client.get(reverse(self.path_name))
        self.assertContains(response, '<title>Главная страница</title>')
