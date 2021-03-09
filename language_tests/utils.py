from language_tests.models import LanguageTestType


class LanguageTestMixin:
    model = LanguageTestType
    queryset = LanguageTestType.objects.filter(is_published=True).only(
        'id',
        'name'
    )
