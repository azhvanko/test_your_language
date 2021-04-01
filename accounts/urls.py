from django.urls import path

from accounts import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<slug:user>/', views.profile, name='profile'),
    path('profile/<slug:user>/activate/<uuid:link>/', views.activate_user, name='activate_user'),
    path('profile/<slug:user>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('profile/<slug:user>/reactivate/', views.reactivate_user, name='reactivate_user'),
    path('signup/', views.signup, name='signup'),
]
