# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0006_remove_referralcredit_customer_referral_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralcredit',
            name='customer_referral_history',
            field=models.ForeignKey(default=1, to='referral.CustomerReferralHistory'),
            preserve_default=False,
        ),
    ]
