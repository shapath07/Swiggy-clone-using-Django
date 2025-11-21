


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserRecord(AbstractUser):
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    discounted_bill = models.FloatField(null=True,blank=True)
    coupon_applied = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='userrecord_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='userrecord_user_permissions'
    )

    def __str__(self):
        return self.username

    


class Category(models.Model):
    restrorent = models.ForeignKey("Restrorent", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    status = models.CharField(max_length=10, choices=[('cart', 'In Cart'), ('ordered', 'Ordered')], default='cart')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ✅ Corrected
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bill_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    group = models.ForeignKey('OrderGroup', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        
        return f"Order of {self.product.name} by {self.user.username}"

    def save(self, *args, **kwargs):
        # ✅ Corrected product reference and renamed field
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

class OrderGroup(models.Model):
    user = models.ForeignKey(UserRecord, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)

    def __str__(self):
        return f"OrderGroup #{self.id} for {self.user.username}"
    
class coupon (models.Model):
    c_name = models.CharField((""), max_length=50)
    
    def __str__(self):
         return self.c_name
    
class Restrorent(models.Model):

    Name = models.CharField( max_length=50 )
    image = models.ImageField( upload_to='restrorents/',null=True,blank=True)

