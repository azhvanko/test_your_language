from django.urls import path

from language_tests.views import LanguageTestListView


urlpatterns = [
    path('', LanguageTestListView.as_view(), name='language_tests'),
]
