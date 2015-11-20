# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0004_referralcredit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreferralhistory',
            name='order',
            field=models.OneToOneField(null=True, blank=True, to='payment.Order'),
        ),
    ]
