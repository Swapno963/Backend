from django.contrib import admin
from .models import Menu, ServiceLocation,Card,Favourite
# Register your models here.
admin.site.register(Menu)
admin.site.register(ServiceLocation)
admin.site.register(Card)
admin.site.register(Favourite)
