from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wallet, Deposit, Withdrawal, Transaction, Ticket, CRYPTO_CHOICES
from .forms import WithdrawalForm, TicketForm


@login_required
def user_dashboard(request):
    wallets = Wallet.objects.filter(user=request.user)
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'wallets': wallets,
        'recent_transactions': recent_transactions,
        'total_balance_coins': wallets.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def spot_wallets(request):
    wallets = Wallet.objects.filter(user=request.user)
    return render(request, 'dashboard/spot-wallets.html', {'wallets': wallets})


@login_required
def wallet_detail(request, coin):
    coin = coin.upper()
    wallet, _ = Wallet.objects.get_or_create(user=request.user, coin=coin)
    deposits = Deposit.objects.filter(user=request.user, coin=coin).order_by('-created_at')
    withdrawals = Withdrawal.objects.filter(user=request.user, coin=coin).order_by('-created_at')
    template = f'dashboard/user/wallet/spot/{coin}.html'
    context = {'wallet': wallet, 'deposits': deposits, 'withdrawals': withdrawals}
    return render(request, template, context)


@login_required
def deposit_history(request):
    deposits = Deposit.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/user/deposit/history.html', {'deposits': deposits})


@login_required
def withdraw_history(request):
    withdrawals = Withdrawal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/user/withdraw/history.html', {'withdrawals': withdrawals})


@login_required
def withdraw_request(request, coin):
    coin = coin.upper()
    wallet = get_object_or_404(Wallet, user=request.user, coin=coin)
    form = WithdrawalForm(request.POST or None, initial={'coin': coin})
    if request.method == 'POST' and form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.wallet = wallet
        withdrawal.save()
        Transaction.objects.create(
            user=request.user,
            transaction_type='withdrawal',
            coin=coin,
            amount=withdrawal.amount,
            status='pending',
        )
        messages.success(request, 'Withdrawal request submitted.')
        return redirect('withdraw_history')
    return render(request, f'dashboard/user/wallet/spot/{coin}.html', {'wallet': wallet, 'form': form})


@login_required
def transactions(request):
    txns = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/transactions.html', {'transactions': txns})


@login_required
def referrals(request):
    refs = request.user.referrals.all()
    return render(request, 'dashboard/referrals.html', {'referrals': refs})


@login_required
def tickets(request):
    user_tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/tickets.html', {'tickets': user_tickets})


@login_required
def new_ticket(request):
    form = TicketForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        messages.success(request, 'Support ticket submitted.')
        return redirect('tickets')
    return render(request, 'dashboard/ticket/new.html', {'form': form})


@login_required
def twofactor(request):
    return render(request, 'dashboard/twofactor.html')


@login_required
def connect_wallet(request):
    return render(request, 'dashboard/connect/connect.html')
