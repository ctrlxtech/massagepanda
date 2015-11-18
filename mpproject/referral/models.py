from django.db import models
from customers.models import Customer
from payment.models import Order
from django.core.validators import MinValueValidator

# Create your models here.
class CustomerReferralCode(models.Model):
    customer = models.OneToOneField(Customer)
    code = models.CharField(max_length=80, db_index=True)

class CustomerReferralHistory(models.Model):
    code = models.ForeignKey(CustomerReferralCode)
    order = models.OneToOneField(Order)
    referred_customer = models.OneToOneField(Customer)
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Success'),
        ('C', 'Cancelled'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

class ReferredCustomer(models.Model):
    code = models.ForeignKey(CustomerReferralCode)
    customer = models.OneToOneField(Customer)
    redeemed = models.BooleanField(default = False)

class ReferralCredit(models.Model):
    customer = models.ForeignKey(Customer)
    customer_referral_history = models.OneToOneField(CustomerReferralHistory)
    credit = models.FloatField(validators = [MinValueValidator(0.00)])
    accumulative_credit = models.FloatField(validators = [MinValueValidator(0.00)])
