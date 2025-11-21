from django.contrib import admin
from django.contrib import admin
from .models import Category,Product,Order,UserRecord,coupon

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(UserRecord)
admin.site.register(coupon)


