# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0003_auto_20151124_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='referralcredit',
            name='adjustment',
            field=models.BooleanField(default=False),
        ),
    ]
