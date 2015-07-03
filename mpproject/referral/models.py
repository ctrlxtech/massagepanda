from django.db import models
from customers.models import Customer
from payment.models import Order

# Create your models here.
class CustomerReferralCode(models.Model):
    customer = models.OneToOneField(Customer)
    code = models.CharField(max_length=80)

class CustomerReferralHistory(models.Model):
    code = models.ForeignKey(CustomerReferralCode)
    referral = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Success'),
        ('C', 'Cancelled'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
