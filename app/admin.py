# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *

class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price')

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('order_number','performed_datetime', 'status', 'customer_id','good_id','order_amount','payment_type')
    list_filter = ('good_id', 'status' )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','phone','email')
    ordering = ['-id']

class LeadAdmin(admin.ModelAdmin):
    list_display = ['time','type','customer_id','payment_id']
    list_filter = ['type']
    ordering = ['-time']



admin.site.register(Goods, GoodsAdmin)
admin.site.register(Payments,PaymentsAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Lead,LeadAdmin)