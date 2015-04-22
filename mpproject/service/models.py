from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Service(models.Model):
    service_type = models.CharField(max_length = 200)
    service_detail = models.CharField(max_length = 200)
    service_time = models.FloatField(max_length = 20, validators = [MinValueValidator(0.0)])
    service_fee = models.FloatField(max_length = 40, validators = [MinValueValidator(0.0)])

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name = 'images')
    image = models.ImageField();
