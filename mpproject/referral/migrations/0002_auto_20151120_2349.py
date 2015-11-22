# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_squashed_0007_referralcredit_customer_referral_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreferralhistory',
            name='referred_customer',
            field=models.OneToOneField(to='customers.Customer'),
        ),
        migrations.AlterField(
            model_name='referralcredit',
            name='customer_referral_history',
            field=models.ForeignKey(to='referral.CustomerReferralHistory'),
        ),
    ]
