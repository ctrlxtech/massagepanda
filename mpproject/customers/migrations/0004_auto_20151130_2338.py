# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20151117_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'0', b'Male'), (b'1', b'Female')]),
        ),
    ]
