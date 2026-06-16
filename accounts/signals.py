from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from dashboard.models import Wallet, CRYPTO_CHOICES


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallets(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.bulk_create([
            Wallet(user=instance, coin=coin) for coin, _ in CRYPTO_CHOICES
        ])
