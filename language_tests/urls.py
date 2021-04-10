from django.urls import path

from language_tests import views


urlpatterns = [
    path('', views.language_tests, name='language_tests'),
    path('<int:pk>/', views.language_test_preview, name='language_test_preview'),
    path('<int:pk>/test/', views.language_test, name='language_test'),
    path('result/', views.test_result, name='test_result'),
]
