from django.urls import path

from language_tests.views import (
    LanguageTestDetailView,
    LanguageTestListView,
    LanguageTestView
)


urlpatterns = [
    path('', LanguageTestListView.as_view(), name='language_tests'),
    path('<int:pk>/', LanguageTestDetailView.as_view(), name='language_test_preview'),
    path('<int:pk>/test', LanguageTestView.as_view(), name='language_test'),
]
