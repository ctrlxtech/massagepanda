# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20150416_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_fee',
            field=models.FloatField(max_length=40, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_time',
            field=models.FloatField(max_length=20, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
