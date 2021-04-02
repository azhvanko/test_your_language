from django.urls import path

from accounts import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password/change/', views.password_change, name='password_change'),
    path('password/change/done/', views.password_change_done, name='password_change_done'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('password/reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('password/reset/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password/reset/done/', views.password_reset_done, name='password_reset_done'),
    path('profile/<slug:user>/', views.profile, name='profile'),
    path('profile/<slug:user>/activate/<uuid:link>/', views.activate_user, name='activate_user'),
    path('profile/<slug:user>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('profile/<slug:user>/reactivate/', views.reactivate_user, name='reactivate_user'),
    path('signup/', views.signup, name='signup'),
]
