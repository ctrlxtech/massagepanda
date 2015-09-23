# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0022_auto_20150921_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='rate_count',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='rating',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
    ]
