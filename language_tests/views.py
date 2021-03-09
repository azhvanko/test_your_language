from django.views.generic import DetailView, ListView

from language_tests.utils import LanguageTestMixin


class LanguageTestListView(LanguageTestMixin, ListView):
    context_object_name = 'language_test_list'
    template_name = 'language_tests/language_tests.html'


class LanguageTestDetailView(LanguageTestMixin, DetailView):
    context_object_name = 'language_test'
    template_name = 'language_tests/language_test_preview.html'
