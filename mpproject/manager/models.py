from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

GENDER_CHOICES = (
    ('0', 'Male'),
    ('1', 'Female'),
)

# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    title = models.PositiveIntegerField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length = 16, validators=[phone_regex], unique=True) # validators should be a list
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_photo = models.ImageField(null=True, blank=True);

    def __unicode__(self):
        return u'%s %s' %(self.first_name, self.last_name)

class Therapist(models.Model):
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must" \
    " be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # validators should be a list
    phone = models.CharField(max_length = 16, validators=[phone_regex], unique=True)
    home_address = models.CharField(max_length = 500)
    availability = models.CharField(max_length = 500)
    working_area = models.CharField(max_length = 500)
    experience = models.CharField(max_length = 500)
    specialty = models.CharField(max_length = 500)
    massage_license = models.ImageField();
    driver_license = models.ImageField();
    emergency_contact_name = models.CharField(max_length = 50)
    emergency_contact_phone = models.CharField(max_length = 16, validators=[phone_regex])
    supplementary = models.CharField(max_length = 500, blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True, default=0)
    rate_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    profile_photo = models.ImageField(null=True, blank=True);
    routing_number = models.IntegerField()
    account_number = models.IntegerField()

    def __unicode__(self):
        return u'%s %s' %(self.user.first_name, self.user.last_name)

class Schedule(models.Model):
    DAY_CHOICES = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    )
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    therapist = models.ForeignKey(Therapist)
    active = models.BooleanField()

    def __unicode__(self):
        return u'%s' %(self.get_day_display())

class Interval(models.Model):
    starttime = models.TimeField()
    endtime = models.TimeField()
    therapist = models.ForeignKey(Schedule)
    def __str__(self):
        return 'starttime:\'%s\',endtime:\'%s\'' %(self.starttime, self.endtime)

class Area(models.Model):
    AREA_CHOICES = (
        ('0', 'San Francisco'),
        ('1', 'Peninsula'),
        ('2', 'East Bay'),
        ('3', 'South Bay'),
    )
    areacode = models.CharField(max_length=10, choices=AREA_CHOICES)
    staff = models.ForeignKey(Staff, null=True, blank=True)
    therapist = models.ForeignKey(Therapist, null=True, blank=True)

    def __unicode__(self):
        return u'%s' %(self.get_areacode_display())

class InSMS(models.Model):
    staff = models.ForeignKey(Staff, null=True)
    sender = models.CharField(max_length = 200)
    messageId = models.CharField(max_length = 200, null=True)
    messageBody = models.CharField(max_length = 1000)
    timestamp = models.CharField(max_length = 200, null=True)

class OutSMS(models.Model):
    staff = models.ForeignKey(Staff, null=True)
    receiver = models.CharField(max_length = 200)
    messageBody = models.CharField(max_length = 1000)
    timestamp = models.CharField(max_length = 200)

class ForwardSMS(models.Model):
    staff = models.ForeignKey(Staff, null=True)
    receiver = models.CharField(max_length = 200)
    messageBody = models.CharField(max_length = 1000)
    timestamp = models.CharField(max_length = 200)

class ForwardNumber(models.Model):
    number = models.ForeignKey(Staff)

class SMSTemplate(models.Model):
    messageBody = models.CharField(max_length = 1000)
