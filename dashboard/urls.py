from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('wallets/', views.spot_wallets, name='spot_wallets'),
    path('wallet/<str:coin>/', views.wallet_detail, name='wallet_detail'),
    path('deposit/history/', views.deposit_history, name='deposit_history'),
    path('withdraw/history/', views.withdraw_history, name='withdraw_history'),
    path('withdraw/<str:coin>/', views.withdraw_request, name='withdraw_request'),
    path('transactions/', views.transactions, name='transactions'),
    path('referrals/', views.referrals, name='referrals'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/new/', views.new_ticket, name='new_ticket'),
    path('2fa/', views.twofactor, name='twofactor'),
    path('connect/', views.connect_wallet, name='connect_wallet'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]
