from django.db import models
from django.core.validators import RegexValidator
from customers.models import Customer
from services.models import Service
from manager.models import Staff

import uuid

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")

    service = models.ForeignKey(Service, default=None, null=True)
    service_datetime = models.DateTimeField()

    GENDER_PREFERENCES = (
        ('0', 'Either'),
        ('1', 'Female Preferred'),
        ('2', 'Male Preferred'),
    )

    preferred_gender = models.CharField(max_length = 10, choices=GENDER_PREFERENCES, default='0')
    need_table = models.BooleanField()
    parking_info = models.CharField(max_length = 500)

    customer = models.ForeignKey(Customer, default=None, null=True)
    stripe_token = models.CharField(max_length = 100)
    amount = models.IntegerField()
    
    shipping_address = models.CharField(max_length = 500)
    recipient = models.CharField(max_length = 50)
    billing_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 16, validators=[phone_regex])
    email = models.EmailField()

    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Confirmed'),
        ('2', 'Shipped'),
        ('3', 'Canceled'),
        ('4', 'Charged'),
        ('5', 'Refunded'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='0')

class OrderTherapist(models.Model):
    order = models.ForeignKey(Order)
    staff = models.ForeignKey(Staff)

class Coupon(models.Model):
    code = models.CharField(max_length=40, unique=True, db_index=True)
    discount = models.FloatField()
