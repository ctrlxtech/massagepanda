from django.db import models
from django.core.validators import RegexValidator
from customers.models import Customer
from services.models import Service

# Create your models here.
class Order(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")

    service = models.ForeignKey(Service, default=None, null=True)
    customer = models.ForeignKey(Customer, default=None, null=True)
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
    
    service = models.ForeignKey(Service, default=None, null=True)
    customer = models.ForeignKey(Customer, default=None, null=True)
    charge_token = models.CharField(max_length = 100)

    shipping_address = models.CharField(max_length = 500)
    name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 16, validators=[phone_regex])
    email = models.EmailField()
    refunded = models.BooleanField(default=False)
'''
class StripeCard(model.Model):
    service = models.ForeignKey(Customer)
    card_id = models.CharField(max_length = 50)
'''
