from django.db import models
from payment.models import Order

import uuid

# Create your models here.
class Feedback(models.Model):
    order = models.OneToOneField(Order)
    RATING_SCALE = (
        ('1', 'Very Poor'),
        ('2', 'Poor'),
        ('3', 'OK'),
        ('4', 'Good'),
        ('5', 'Very Good'),
    )
    rating = models.CharField(max_length=1, choices=RATING_SCALE, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    code = models.UUIDField(default=uuid.uuid1, editable=False, unique=True, db_index=True)
    request_count = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    rated = models.BooleanField()
