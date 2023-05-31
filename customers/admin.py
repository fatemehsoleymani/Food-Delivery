from django.contrib import admin
from customers.models import MenuItem, Category, OrderModel

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
