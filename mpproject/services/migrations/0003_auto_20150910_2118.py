# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_service_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_fee',
            field=models.DecimalField(max_digits=6, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_sale',
            field=models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_time',
            field=models.DecimalField(max_digits=6, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
