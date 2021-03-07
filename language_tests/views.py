from django.views.generic import ListView

from language_tests.models import LanguageTestType


class LanguageTestListView(ListView):
    context_object_name = 'language_test_list'
    model = LanguageTestType
    queryset = LanguageTestType.objects.filter(is_published=True).only('id', 'name')
    template_name = 'language_tests/language_tests.html'
