# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20150523_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='stripe_customer_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
