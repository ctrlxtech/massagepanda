# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0023_ordertherapist_order'),
        ('referral', '0005_remove_customerreferralhistory_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerreferralhistory',
            name='order',
            field=models.OneToOneField(default=1, to='payment.Order'),
            preserve_default=False,
        ),
    ]
