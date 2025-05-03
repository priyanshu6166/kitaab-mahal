from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, unique=True)
    is_mobile_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.mobile_number}"

class OTP(models.Model):
    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mobile_number} - {self.otp}"

    @classmethod
    def generate_otp(cls):
        return ''.join(random.choices(string.digits, k=6))
