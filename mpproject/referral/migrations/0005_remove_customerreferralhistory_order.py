# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0004_customerreferralhistory_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerreferralhistory',
            name='order',
        ),
    ]
