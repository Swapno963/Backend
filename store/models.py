from django.db import models
from accounts.models import CustomUser


class ServiceLocation(models.Model):
    address =models.CharField(max_length=50)

    def __str__(self):
        return self.address


class Card(models.Model):
    card_id = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    is_active = models.BooleanField(default=False)
    is_feature = models.BooleanField(default=False)
    service_location = models.ForeignKey(ServiceLocation, 
                                        on_delete=models.SET_DEFAULT, 
                                        default=None)

    def __str__(self):
        return self.title



class Menu(models.Model):
    name = models.CharField(max_length=255)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True,blank=True, related_name='menus')
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    menu_id = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    card = models.ForeignKey(Card, on_delete=models.SET_DEFAULT, default=None)