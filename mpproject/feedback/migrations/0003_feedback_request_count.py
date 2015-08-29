# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20150819_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='request_count',
            field=models.DecimalField(default=0, max_digits=1, decimal_places=0),
        ),
    ]
