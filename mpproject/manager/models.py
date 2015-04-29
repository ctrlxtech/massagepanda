from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Staff(models.Model):
    name = models.CharField(max_length = 200)
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length = 16, validators=[phone_regex], blank=True) # validators should be a list
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_photo = models.ImageField();
