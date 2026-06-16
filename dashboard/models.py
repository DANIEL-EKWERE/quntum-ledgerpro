from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


CRYPTO_CHOICES = [
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('BNB', 'BNB'),
    ('SOL', 'Solana'),
    ('ADA', 'Cardano'),
    ('XRP', 'XRP'),
    ('USDT', 'Tether USDT'),
    ('USDC', 'USD Coin'),
    ('DOGE', 'Dogecoin'),
    ('TRX', 'TRON'),
    ('XLM', 'Stellar'),
]

TRANSACTION_STATUS = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    coin = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    address = models.CharField(max_length=255, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'coin')

    def __str__(self):
        return f"{self.user.email} - {self.coin}"


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='deposits')
    coin = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    txid = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Deposit {self.coin} {self.amount} by {self.user.email}"


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, related_name='withdrawals')
    coin = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Withdrawal {self.coin} {self.amount} by {self.user.email}"


class Transaction(models.Model):
    TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('bonus', 'Bonus'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPES)
    coin = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='pending')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.coin} {self.amount} - {self.user.email}"


class Ticket(models.Model):
    PRIORITY = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.pk} - {self.subject}"


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to Ticket #{self.ticket.pk}"
