# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_schedule_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapist',
            name='account_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='therapist',
            name='routing_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
