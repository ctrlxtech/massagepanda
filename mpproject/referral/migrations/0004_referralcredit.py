# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customercredit'),
        ('referral', '0003_auto_20151016_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('accumulative_credit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('customer', models.ForeignKey(to='customers.Customer')),
                ('customer_referral_history', models.OneToOneField(to='referral.CustomerReferralHistory')),
            ],
        ),
    ]
