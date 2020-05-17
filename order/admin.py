from django.contrib import admin

# Register your models here.
from order.models import ShopCart

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'amount']
    list_filter = ['user']
    # readonly_fields = ('user', 'quantity')

admin.site.register(ShopCart, ShopCartAdmin)