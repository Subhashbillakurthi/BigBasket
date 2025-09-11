from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    weight = models.CharField(max_length=50, null=True, blank=True)   # e.g. "500g", "1kg"
    weight_250g = models.CharField(max_length=50, null=True, blank=True)
    price_250g = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    mrp = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price_per_g = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    image1 = models.CharField(max_length=500, blank=True, null=True)
    image2 = models.CharField(max_length=500, blank=True, null=True)
    image3 = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Pack(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='packs'  # This enables product.packs.all()
    )
    weight = models.CharField(max_length=50)
    mrp = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_g = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    # Add any extra fields for pack, e.g. earliest_delivery etc.

    def __str__(self):
        return f"{self.weight} ({self.product.name})"
    

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # A product appears once per user

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    


