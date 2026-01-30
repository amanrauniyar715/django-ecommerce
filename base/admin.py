from django.contrib import admin
from .models import Luggage, Cart, Order
# Register your models here.
admin.site.register(Luggage)
admin.site.register(Cart)
admin.site.register(Order)


admin.site.site_header = "Urban Luggage Admin"
admin.site.site_title = "Urban Luggage"
admin.site.index_title = "Welcome to Urban Luggage Dashboard"
