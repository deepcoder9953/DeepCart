from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return self.name

class ShowProduct(models.Model):
    img = models.ImageField(upload_to='image', null=True, blank=True)
    name = models.CharField(max_length=20)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    img = models.ImageField(upload_to= 'image/', default='img.jpg')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

class RegisterUser(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=10)
    last_login = models.DateTimeField(null=True, blank=True)

    def get_email_field_name(self):
        return 'email'

    def __def__(self):
        return self.name

