from celery import shared_task
from .models import BlacklistedToken
from datetime import timedelta
from django.utils import timezone


@shared_task
def task1():
    print("Generating PDF...")

@shared_task
def task2():
    print("Sending notification...")


@shared_task
def remove_expired_tokens():
	now = timezone.now()   
	expiration_time = now - timedelta(hours=12)

	expired_tokens = BlacklistedToken.objects.filter(blacklisted_at__lte=expiration_time)
	expired_tokens_count = expired_tokens.count()
	expired_tokens.delete()

	print(f"Deleted {expired_tokens_count} expired blacklisted access tokens. ")