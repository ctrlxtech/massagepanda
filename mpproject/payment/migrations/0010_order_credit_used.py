# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20151108_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='credit_used',
            field=models.FloatField(default=0.0),
        ),
    ]
