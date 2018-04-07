from django.contrib import admin
from .models import *

admin.site.register(product)
admin.site.register(product_description)
admin.site.register(shopping_cart_items)
admin.site.register(addresses)
admin.site.register(all_orders_table)
