from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phone_number = models.CharField(max_length = 16, validators=[phone_regex], unique=True)
    email = models.EmailField()

class Address(models.Model):
    address_line1 = models.CharField("Address line 1", max_length = 45)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10)
    city = models.CharField(max_length = 50, blank = False)
    state_province = models.CharField("State/Province", max_length = 40, blank = True)
    country = models.CharField(max_length = 45, blank = False)

    customer = models.ForeignKey(Customer, blank = False)
    def __unicode__(self):
        return "%s, %s %s" % (self.city, self.state_province,
                              str(self.country))
