import debug_toolbar
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('home.urls')),
    path('tests/', include('language_tests.urls')),
]
