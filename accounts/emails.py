from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import threading


def _send(subject, to_email, template, context):
    """Send an HTML email in a background thread so views don't block."""
    def _worker():
        try:
            html = render_to_string(template, context)
            text = f"{subject}\n\nPlease view this email in an HTML-capable email client."
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )
            msg.attach_alternative(html, "text/html")
            msg.send(fail_silently=True)
        except Exception:
            pass  # never crash a view due to email failure

    threading.Thread(target=_worker, daemon=True).start()


def send_welcome_email(user):
    _send(
        subject="Welcome to QuantumLedgerPro!",
        to_email=user.email,
        template="emails/welcome.html",
        context={"user": user},
    )


def send_login_notification(user, request):
    _send(
        subject="New sign-in to your QuantumLedgerPro account",
        to_email=user.email,
        template="emails/login_notification.html",
        context={
            "user": user,
            "ip": _get_ip(request),
            "device": request.META.get("HTTP_USER_AGENT", "Unknown device"),
        },
    )


def send_deposit_confirmation(user, deposit):
    _send(
        subject=f"Deposit Request Received — {deposit.coin}",
        to_email=user.email,
        template="emails/deposit_confirmation.html",
        context={"user": user, "deposit": deposit},
    )
    # Also alert admin
    _send(
        subject=f"[Admin] New Deposit: {user.email} — {deposit.amount} {deposit.coin}",
        to_email=settings.ADMIN_EMAIL,
        template="emails/admin_deposit_alert.html",
        context={"user": user, "deposit": deposit},
    )


def send_withdrawal_confirmation(user, withdrawal):
    _send(
        subject=f"Withdrawal Request Received — {withdrawal.coin}",
        to_email=user.email,
        template="emails/withdrawal_confirmation.html",
        context={"user": user, "withdrawal": withdrawal},
    )
    _send(
        subject=f"[Admin] New Withdrawal: {user.email} — {withdrawal.amount} {withdrawal.coin}",
        to_email=settings.ADMIN_EMAIL,
        template="emails/admin_withdrawal_alert.html",
        context={"user": user, "withdrawal": withdrawal},
    )


def send_wallet_connected(user, connected_wallet):
    _send(
        subject=f"Wallet Linked — {connected_wallet.wallet_name}",
        to_email=user.email,
        template="emails/wallet_connected.html",
        context={"user": user, "wallet": connected_wallet},
    )
    _send(
        subject=f"[Admin] Wallet Linked: {user.email} — {connected_wallet.wallet_name}",
        to_email=settings.ADMIN_EMAIL,
        template="emails/admin_wallet_alert.html",
        context={"user": user, "wallet": connected_wallet},
    )


def send_ticket_confirmation(user, ticket):
    _send(
        subject=f"Support Ticket #{ticket.pk} Received",
        to_email=user.email,
        template="emails/ticket_confirmation.html",
        context={"user": user, "ticket": ticket},
    )


def _get_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR", "Unknown")
