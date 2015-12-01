# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20151130_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(max_length=10, choices=[(b'0', b'Monday'), (b'1', b'Tuesday'), (b'2', b'Wednesday'), (b'3', b'Thursday'), (b'4', b'Friday'), (b'5', b'Saturday'), (b'6', b'Sunday')]),
        ),
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'0', b'Male'), (b'1', b'Female')]),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'0', b'Male'), (b'1', b'Female')]),
        ),
    ]
