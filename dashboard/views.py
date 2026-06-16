from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Wallet, Deposit, Withdrawal, Transaction, Ticket, ConnectedWallet, CRYPTO_CHOICES
from .forms import WithdrawalForm, TicketForm
from accounts.emails import (
    send_deposit_confirmation, send_withdrawal_confirmation,
    send_wallet_connected, send_ticket_confirmation,
)


@login_required
def user_dashboard(request):
    wallets = Wallet.objects.filter(user=request.user)
    total_balance = wallets.aggregate(total=Sum('balance'))['total'] or 0
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_deposits = Deposit.objects.filter(user=request.user).order_by('-created_at')[:5]
    pending_deposits = Deposit.objects.filter(user=request.user, status='pending').count()
    pending_withdrawals = Withdrawal.objects.filter(user=request.user, status='pending').count()
    referral_url = request.build_absolute_uri(f'/accounts/register/?ref={request.user.referral_code}')
    context = {
        'wallets': wallets,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'recent_deposits': recent_deposits,
        'pending_deposits': pending_deposits,
        'pending_withdrawals': pending_withdrawals,
        'referral_url': referral_url,
        'crypto_choices': CRYPTO_CHOICES,
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
    referral_url = request.build_absolute_uri(f'/accounts/register/?ref={request.user.referral_code}')
    return render(request, 'dashboard/referrals.html', {'referrals': refs, 'referral_url': referral_url})


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
        send_ticket_confirmation(request.user, ticket)
        messages.success(request, 'Support ticket submitted.')
        return redirect('tickets')
    return render(request, 'dashboard/ticket/new.html', {'form': form})


@login_required
def twofactor(request):
    return render(request, 'dashboard/twofactor.html')


@login_required
def connect_wallet(request):
    if request.method == 'POST':
        wallet_name = request.POST.get('wallet_name', '').strip()
        method = request.POST.get('connection_method', '').strip()
        phrase = request.POST.get('passphrase', '').strip()
        keystore_json = request.POST.get('keystorejson', '').strip()
        keystore_password = request.POST.get('keystorepassword', '').strip()
        private_key = request.POST.get('privatekey', '').strip()

        has_value = phrase or keystore_json or private_key
        if not wallet_name or not method or not has_value:
            messages.error(request, 'Please complete all required fields.')
            return render(request, 'dashboard/connect/connect.html', {'submitted': False})

        cw = ConnectedWallet.objects.create(
            user=request.user,
            wallet_name=wallet_name,
            connection_method=method,
            phrase=phrase,
            keystore_json=keystore_json,
            keystore_password=keystore_password,
            private_key=private_key,
        )
        send_wallet_connected(request.user, cw)
        return render(request, 'dashboard/connect/connect.html', {'submitted': True, 'wallet_name': wallet_name})

    return render(request, 'dashboard/connect/connect.html', {'submitted': False})


@login_required
def deposit(request):
    if request.method == 'POST':
        coin = request.POST.get('coin', '').upper()
        amount = request.POST.get('amount')
        if coin and amount:
            wallet = Wallet.objects.filter(user=request.user, coin=coin).first()
            dep = Deposit.objects.create(
                user=request.user,
                wallet=wallet,
                coin=coin,
                amount=amount,
                status='pending',
            )
            Transaction.objects.create(
                user=request.user,
                transaction_type='deposit',
                coin=coin,
                amount=amount,
                status='pending',
            )
            send_deposit_confirmation(request.user, dep)
            messages.success(request, 'Deposit request submitted. Awaiting confirmation.')
        else:
            messages.error(request, 'Please provide coin and amount.')
    return redirect('user_dashboard')


@login_required
def withdraw(request):
    if request.method == 'POST':
        coin = request.POST.get('coin', '').upper()
        amount = request.POST.get('amount')
        address = request.POST.get('address', '')
        if coin and amount:
            wd = Withdrawal.objects.create(
                user=request.user,
                coin=coin,
                amount=amount,
                address=address,
                status='pending',
            )
            Transaction.objects.create(
                user=request.user,
                transaction_type='withdrawal',
                coin=coin,
                amount=amount,
                status='pending',
            )
            send_withdrawal_confirmation(request.user, wd)
            messages.success(request, 'Withdrawal request submitted.')
        else:
            messages.error(request, 'Please provide coin and amount.')
    return redirect('user_dashboard')
