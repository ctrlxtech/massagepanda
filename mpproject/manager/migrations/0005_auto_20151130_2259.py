# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20151014_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='areacode',
            field=models.CharField(max_length=10, choices=[(0, b'San Francisco'), (1, b'Peninsula'), (2, b'East Bay'), (3, b'South Bay')]),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(max_length=10, choices=[(0, b'Monday'), (1, b'Tuesday'), (2, b'Wednesday'), (3, b'Thursday'), (4, b'Friday'), (5, b'Saturday'), (6, b'Sunday')]),
        ),
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(max_length=1, choices=[(0, b'Male'), (1, b'Female')]),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='gender',
            field=models.CharField(max_length=1, choices=[(0, b'Male'), (1, b'Female')]),
        ),
    ]
