from django import forms
from .models import Withdrawal, Ticket


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['coin', 'amount', 'address']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'message', 'priority']
