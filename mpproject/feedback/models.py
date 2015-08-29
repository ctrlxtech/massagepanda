from django.db import models
from payment.models import Order

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
    code = models.CharField(max_length=40, db_index=True)
    request_count = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    rated = models.BooleanField()
