# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerReferralCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=80)),
                ('customer', models.OneToOneField(to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerReferralHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=1, choices=[(b'P', b'Pending'), (b'S', b'Success'), (b'C', b'Cancelled')])),
                ('code', models.ForeignKey(to='referral.CustomerReferralCode')),
                ('order', models.OneToOneField(to='payment.Order')),
            ],
        ),
    ]
