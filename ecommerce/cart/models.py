from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order_details(models.Model):
    product=models.ForeignKey (Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    address=models.TextField()
    phone=models.BigIntegerField()
    pin=models.IntegerField()
    order_id=models.CharField(max_length=30)
    payment_status=models.CharField(max_length=30, default="pending")
    delivery_status=models. CharField(max_length=30, default="pending")
    ordered_date=models.DateTimeField(auto_now_add=True)
    def _str__(self):
        return self.order_id


class Payment(models. Model):
    name=models.CharField(max_length=30)
    amount=models. IntegerField()
    order_id=models.CharField(max_length=30)
    razorpay_payment_id=models.CharField(max_length=30, blank=True)
    paid=models.BooleanField(default=False)
    def str(self):
        return self.order_id