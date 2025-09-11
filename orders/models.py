from django.db import models
from django.contrib.auth.models import User

class DeliverySlot(models.Model):
    date = models.DateField()
    slot_label = models.CharField(max_length=64)  # e.g. "7:00 AM - 10:00 AM"

    def __str__(self):
        return f"{self.date.strftime('%a, %d %b')} {self.slot_label}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Placed'),
        ('In Process', 'In Process'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Reached', 'Reached'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,blank=True, null=True)
    delivery_slot = models.ForeignKey(DeliverySlot, on_delete=models.SET_NULL, null=True)
    placed_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    savings = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Placed')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.CharField(max_length=128)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True, null=True)
    mrp = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)
