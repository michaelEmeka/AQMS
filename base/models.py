# Create your models here.
from django.db import models
class Tank(models.Model):
    user_address = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)
    last_filled = models.DateTimeField(auto_now_add=True)
    is_pumping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    water_level = models.IntegerField(default=0)

    def __str__(self):
        return self.user_address
