from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Service(models.Model):
    service_type = models.CharField(max_length = 200)
    service_detail = models.CharField(max_length = 200)
    service_time = models.FloatField(max_length = 20, validators = [MinValueValidator(0.0)])
    service_sale = models.FloatField(max_length = 40, validators = [MinValueValidator(0.00)], null=True, blank=True)
    service_fee = models.FloatField(max_length = 40, validators = [MinValueValidator(0.00)])
    
    def __unicode__(self):
        return u'%s %s' % (self.service_type, self.service_time)

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name = 'images')
    image = models.ImageField();
