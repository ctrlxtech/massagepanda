from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Order(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    token = models.CharField(max_length = 100)
    amount = models.IntegerField()
    b_phone = models.CharField(max_length = 16, validators=[phone_regex])
    b_email = models.EmailField()   
    
    shipping_address = models.CharField(max_length = 500)
    name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 16, validators=[phone_regex])
    email = models.EmailField()

    charged = models.BooleanField(default=False)

class Charge(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    token = models.CharField(max_length = 100)

    shipping_address = models.CharField(max_length = 500)
    name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 16, validators=[phone_regex])
    email = models.EmailField()
