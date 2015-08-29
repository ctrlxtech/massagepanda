# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_sale',
            field=models.FloatField(blank=True, max_length=40, null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
