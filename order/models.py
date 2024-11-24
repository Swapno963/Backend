from django.db import models
from accounts.models import UserProfile
# Create your models here.
class Order(models.Model):
    card_code = models.CharField(max_length=3)
    delivery_date = models.DateTimeField()
    sended_by_supplier = models.BooleanField(default=False)
    received_by_admin = models.BooleanField(default=False)
    status = models.CharField(max_length=50)



class Payment(models.Model):
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=50)
    customer_id = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT,default=None)
    payment_invoice = models.IntegerField()
    status = models.CharField(max_length=50)


    