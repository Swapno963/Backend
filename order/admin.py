from django.contrib import admin
from .models import Order, Payment




class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'card_code', 'delivery_date', 'sended_by_supplier', 'received_by_admin', 'status', 'supplier')
    list_filter = ('sended_by_supplier', 'received_by_admin', 'status', 'supplier')
    search_fields = ('card_code', 'supplier__name')  
    ordering = ('-delivery_date',)
admin.site.register(Order, OrderAdmin)




class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'email','payment_method', 'customer_id', 'payment_invoice', 'status', 'order')
    list_filter = ('payment_method', 'status')  
    search_fields = ('payment_invoice', 'customer_id__user', 'order__id')  
admin.site.register(Payment, PaymentAdmin)