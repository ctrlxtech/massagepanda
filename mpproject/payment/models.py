from django.db import models
from django.core.validators import RegexValidator
from customers.models import Customer
from services.models import Service
from manager.models import Staff

# Create your models here.
class Order(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")

    service = models.ForeignKey(Service, default=None, null=True)
    service_datetime = models.DateTimeField()
    preferred_gender = models.CharField(max_length = 20)
    customer = models.ForeignKey(Customer, default=None, null=True)
    token = models.CharField(max_length = 100)
    amount = models.IntegerField()
    
    shipping_address = models.CharField(max_length = 500)
    recipient = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 16, validators=[phone_regex])
    email = models.EmailField()

    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Confirmed'),
        ('2', 'Shipped'),
        ('3', 'Canceled'),
        ('4', 'Refunded'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='0')

class OrderTherapist(models.Model):
    order = models.ForeignKey(Order)
    staff = models.ForeignKey(Staff)
