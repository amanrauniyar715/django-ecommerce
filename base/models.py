from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models

class Luggage(models.Model):
    CATEGORY_CHOICES = [
        ('new', 'New'),
        ('luggage', 'Luggage'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    offer = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='luggage')

    def __str__(self):
        return self.name

class Cart(models.Model):  # fixed `models.Models` to `models.Model`
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Luggage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} in cart"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Luggage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product} for {self.user.username}"



# models.py (continued)
# base/models.py

from django.db import models

class OrderPlacement(models.Model):
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    address = models.TextField()
    email = models.EmailField()
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product_name}"


  # if Luggage is in the same file, you can remove this

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirm', 'Confirm'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    luggage = models.ForeignKey('Luggage', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    shipping_address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # tracking_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)

    def __str__(self):
        return f"Order {self.id} - {self.status}"



