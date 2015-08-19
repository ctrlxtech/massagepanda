# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0019_forwardsms'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='rate',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='rate_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='therapist',
            name='rate',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='therapist',
            name='rate_count',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
