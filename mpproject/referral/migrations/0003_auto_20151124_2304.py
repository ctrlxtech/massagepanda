# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20151108_1608'),
        ('referral', '0002_auto_20151120_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralcredit',
            name='order',
            field=models.OneToOneField(null=True, blank=True, to='payment.Order'),
        ),
        migrations.AlterField(
            model_name='referralcredit',
            name='credit',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='referralcredit',
            name='customer_referral_history',
            field=models.ForeignKey(blank=True, to='referral.CustomerReferralHistory', null=True),
        ),
    ]
