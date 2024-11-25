from django.db import models
from accounts.models import CustomUser


class ServiceLocation(models.Model):
    address =models.CharField(max_length=50)

    def __str__(self):
        return self.address


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    card_id = models.PositiveIntegerField(unique=True, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    is_active = models.BooleanField(default=False)
    service_location = models.ForeignKey(ServiceLocation, 
                                        on_delete=models.SET_DEFAULT, 
                                        default=None)

    def save(self, *args, **kwargs):
        if not self.menu_id:
            super(Card, self).save(*args, **kwargs)  
            self.card_id = self.id + 600  
            self.save(update_fields=['card_id'])  

        else:
            super(Card, self).save(*args, **kwargs) 
    def __str__(self):
        return self.title



class Menu(models.Model):
    name = models.CharField(max_length=255)
    card = models.ForeignKey(Card, on_delete=models.SET_DEFAULT, related_name='menus', default=None)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    menu_id = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    pass



class Favourite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)    
    card = models.ForeignKey(Card, on_delete=models.SET_DEFAULT, default=None)