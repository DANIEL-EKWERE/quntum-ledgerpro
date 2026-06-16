from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('crypto/', views.crypto, name='crypto'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
    path('trade-policy/', views.trade_policy, name='trade_policy'),
]
