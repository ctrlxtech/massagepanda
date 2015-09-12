# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0020_auto_20150911_2153'),
        ('referral', '0003_remove_customerreferralhistory_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerreferralhistory',
            name='order',
            field=models.OneToOneField(default=1, to='payment.Order'),
            preserve_default=False,
        ),
    ]
