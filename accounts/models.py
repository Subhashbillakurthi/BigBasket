from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)  # 5 min validity
    
@receiver(post_save, sender=User)
def create_email_otp(sender, instance, created, **kwargs):
    if created:
        EmailOTP.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=32, blank=True)
    promotions = models.BooleanField(default=True)
    # Add other fields as per need

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line = models.TextField()
    city = models.CharField(max_length=64)
    # ...other fields...
    is_default = models.BooleanField(default=False)

from django.contrib import admin
from products.models import WishlistItem

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)



