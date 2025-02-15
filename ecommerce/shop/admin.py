from django.contrib import admin

# Register your models here.
from shop.models import Product,Category
admin.site.register(Category)
admin.site.register(Product)

