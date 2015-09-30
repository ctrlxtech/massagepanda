# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
        ('customers', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=40, db_index=True)),
                ('discount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('service_datetime', models.DateTimeField()),
                ('preferred_gender', models.CharField(default=b'0', max_length=10, choices=[(b'0', b'Either'), (b'1', b'Female Preferred'), (b'2', b'Male Preferred')])),
                ('need_table', models.BooleanField()),
                ('parking_info', models.CharField(max_length=500)),
                ('stripe_token', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('shipping_address', models.CharField(max_length=500)),
                ('recipient', models.CharField(max_length=50)),
                ('billing_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(default=b'0', max_length=10, choices=[(b'0', b'Pending'), (b'1', b'Confirmed'), (b'2', b'Shipped'), (b'3', b'Canceled'), (b'4', b'Charged'), (b'5', b'Refunded')])),
                ('customer', models.ForeignKey(default=None, blank=True, to='customers.Customer', null=True)),
                ('service', models.ForeignKey(default=None, to='services.Service', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderTherapist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.ForeignKey(to='payment.Order')),
                ('therapist', models.ForeignKey(to='manager.Therapist')),
            ],
        ),
    ]
