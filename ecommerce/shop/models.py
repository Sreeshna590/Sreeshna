from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # ✅ Fix path (no 'media/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # ✅ Fix path
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)  # One-time
    updated = models.DateTimeField(auto_now=True)  # Updated on changes

    def __str__(self):
        return self.name
