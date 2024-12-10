from django.db import models
from accounts.models import UserProfile,SupplierProfile, CustomUser
from store.models import Card
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.


@receiver(pre_delete, sender=UserProfile)
def update_phone_on_userprofile_delete(sender, instance, **kwargs):
    payments = Payment.objects.filter(customer_id=instance)
    
    for payment in payments:
        payment.email = instance.user.email if instance.user else "0000000000"
        payment.customer = None
        payment.save()


class Order(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DELIVERED = 'delivered'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DELIVERED, 'Delivered'),
    ]
    
    card_code = models.CharField(max_length=3)
    delivery_date = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING,
    )
    is_paid = models.BooleanField(default=False)
    card = models.ForeignKey(Card, on_delete=models.CASCADE,blank=True, null=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT,default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.card



class Payment(models.Model):

    email = models.CharField(max_length=30, null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    sender_number = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=50)
    total_amount = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.SET_DEFAULT,default=None)
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_DEFAULT,default=None, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_confirmed:
            self.order.status = Order.ACCEPTED
            self.order.save()

    def __str__(self):
        supplier_user = str(self.order) if self.order  else "No Order"
        customer_user = str(self.customer.user) if self.customer and self.customer.user else "No Customer"
        return f"{supplier_user}---{customer_user}"


