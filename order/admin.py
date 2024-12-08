from django.contrib import admin
from .models import Order, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'card_code', 'delivery_date', 'status')
    list_filter = ('status',)
    search_fields = ('card_code',)  
    ordering = ('-delivery_date',)
admin.site.register(Order, OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','payment_method', 'total_amount', 'customer_id', 'order')
    list_filter = ('payment_method',)  
    search_fields = ('customer_id__user', 'order__id')  
admin.site.register(Payment, PaymentAdmin)
