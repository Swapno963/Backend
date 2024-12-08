from django.db import models
from accounts.models import UserProfile,SupplierProfile
from store.models import Card
from django.db.models.signals import pre_delete
from django.dispatch import receiver



@receiver(pre_delete, sender=UserProfile)
def update_phone_on_userprofile_delete(sender, instance, **kwargs):
    payments = Payment.objects.filter(customer_id=instance)
    
    for payment in payments:
        payment.email = instance.user.email if instance.user else "0000000000"
        payment.customer = None  # Clear the ForeignKey
        payment.save()


# Create your models here.
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
    supplier = models.ForeignKey(SupplierProfile,on_delete=models.SET_DEFAULT,default=None, null=True)
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT,default=None, null=True)


    def __str__(self):
        supplier_user = str(self.supplier.user) if self.supplier and self.supplier.user else "No Supplier"
        customer_user = str(self.customer.user) if self.customer and self.customer.user else "No Customer"
        return f"{supplier_user}---{customer_user}"



class Payment(models.Model):
    email = models.CharField(max_length=30, null=True, blank=True) # this is for storeing email if user profile is deleted
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=50)
    payment_invoice = models.IntegerField()
    status = models.CharField(max_length=50)

    order = models.ForeignKey(Order, on_delete=models.SET_DEFAULT,default=None)
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT,default=None, null=True)

    def __str__(self):
        supplier_user = str(self.order) if self.order  else "No Order"
        customer_user = str(self.customer.user) if self.customer and self.customer.user else "No Customer"
        return f"{supplier_user}---{customer_user}"


