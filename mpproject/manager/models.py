from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    title = models.PositiveIntegerField(max_length = 5) 
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length = 16, validators=[phone_regex], blank=True) # validators should be a list
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_photo = models.ImageField(null=True, blank=True);

class InSMS(models.Model):
    sender = models.CharField(max_length = 200)
    messageId = models.CharField(max_length = 200, null=True)
    messageBody = models.CharField(max_length = 1000)
    timestamp = models.CharField(max_length = 200, null=True)

class OutSMS(models.Model):
    receiver = models.CharField(max_length = 200)
    messageBody = models.CharField(max_length = 1000)
    timestamp = models.CharField(max_length = 200)
