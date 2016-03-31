from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

# Create your models here.
class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    service_type = models.CharField(max_length = 200)
    service_detail = models.CharField(max_length = 200)
    service_time = models.FloatField(validators = [MinValueValidator(0.0)])
    service_sale = models.FloatField(validators = [MinValueValidator(0.00)], null=True, blank=True)
    service_fee = models.FloatField(validators = [MinValueValidator(0.00)])
    labor_cost = models.FloatField(validators = [MinValueValidator(0.00)])
    tip_percent = models.FloatField(validators = [MinValueValidator(0.00)], default=0.00)
    popularity = models.IntegerField()
    
    def __unicode__(self):
        if self.service_sale and self.service_sale > 0:
          return u'%s %s - $%s' % (self.service_type, self.service_time, self.service_sale)
        else:
          return u'%s %s - $%s' % (self.service_type, self.service_time, self.service_fee)

    def link(self):
        if self.service_time > 1:
          return "In-Home_%s_for_%s_Hours" % (self.service_type.replace(' ', '_'), self.service_time)
        else:
          return "In-Home_%s_for_%d_Hour" % (self.service_type.replace(' ', '_'), self.service_time)

class Group(models.Model):
    group_name = models.CharField(max_length = 200)

class ServiceGroup(models.Model):
    service = models.ForeignKey(Service)
    group = models.ForeignKey(Group)

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name = 'images')
    image = models.ImageField();
