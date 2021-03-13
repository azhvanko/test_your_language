from typing import Dict

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from language_tests.models import LanguageTestType
from language_tests.utils import generate_questions_list


class LanguageTestMixin:
    model = LanguageTestType
    queryset = LanguageTestType.objects.filter(is_published=True).only(
        'id',
        'name'
    )


class LanguageTestListView(LanguageTestMixin, ListView):
    context_object_name = 'language_test_list'
    template_name = 'language_tests/language_tests.html'


class LanguageTestDetailView(LanguageTestMixin, DetailView):
    context_object_name = 'language_test'
    template_name = 'language_tests/language_test_preview.html'


class LanguageTestView(LanguageTestMixin, ListView):
    object_list = None
    template_name = 'language_tests/language_test.html'

    def get(self, request, *args, **kwargs):
        get_object_or_404(self.queryset, pk=kwargs['pk'])
        context = self.get_context_data(
            test_type_id=kwargs['pk'],
            user_id=request.user.id
        )

        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs) -> Dict:
        context = super().get_context_data()
        context['questions'] = generate_questions_list(
            test_type_id=kwargs['test_type_id'],
            user_id=kwargs['user_id']
        )
        context['language_test'] = self.model.objects.get(
            id=kwargs['test_type_id']
        )

        return context
