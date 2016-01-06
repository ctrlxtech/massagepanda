# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20151207_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='staff',
            name='vitality',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='therapist',
            name='suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='therapist',
            name='vitality',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
