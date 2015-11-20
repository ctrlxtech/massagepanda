# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0005_auto_20151119_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referralcredit',
            name='customer_referral_history',
        ),
    ]
