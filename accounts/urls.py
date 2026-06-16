from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user-data/', views.user_data, name='user_data'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
]
