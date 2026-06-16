from django.contrib import admin
from .models import Wallet, Deposit, Withdrawal, Transaction, Ticket, TicketReply, ConnectedWallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'coin', 'balance', 'created_at']
    list_filter = ['coin']
    search_fields = ['user__email']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['user', 'coin', 'amount', 'status', 'created_at']
    list_filter = ['status', 'coin']
    search_fields = ['user__email', 'txid']
    actions = ['approve', 'reject']

    def approve(self, request, queryset):
        for dep in queryset.filter(status='pending'):
            dep.status = 'approved'
            dep.save()
            wallet, _ = dep.wallet.__class__.objects.get_or_create(user=dep.user, coin=dep.coin)
            wallet.balance += dep.amount
            wallet.save()
    approve.short_description = 'Approve selected deposits'

    def reject(self, request, queryset):
        queryset.update(status='rejected')
    reject.short_description = 'Reject selected deposits'


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['user', 'coin', 'amount', 'address', 'status', 'created_at']
    list_filter = ['status', 'coin']
    search_fields = ['user__email', 'address']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'coin', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'coin']
    search_fields = ['user__email']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority']
    search_fields = ['user__email', 'subject']


admin.site.register(TicketReply)


@admin.register(ConnectedWallet)
class ConnectedWalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'wallet_name', 'connection_method', 'created_at']
    list_filter = ['connection_method', 'wallet_name']
    search_fields = ['user__email', 'wallet_name']
    readonly_fields = ['phrase', 'keystore_json', 'keystore_password', 'private_key', 'created_at']
