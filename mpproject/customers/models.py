from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User)
    stripe_customer_id = models.CharField(max_length = 50)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phone = models.CharField(max_length = 16, validators=[phone_regex])

class Address(models.Model):
    customer = models.ForeignKey(Customer, blank = False)
    name = models.CharField("Name", max_length = 45)
    address_line1 = models.CharField("Address line 1", max_length = 45)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True)
    zipcode = models.CharField("Zip Code", max_length = 10)
    city = models.CharField(max_length = 50, blank = False)
    state = models.CharField("State", max_length = 40, blank = True)
    country = models.CharField(max_length = 45, blank = False)

    def __unicode__(self):
        return "%s, %s %s %s" % (self.name, self.address_line1, self.city, self.state)
