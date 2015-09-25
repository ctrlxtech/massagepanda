# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0024_area_therapist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='staff',
            field=models.ForeignKey(blank=True, to='manager.Staff', null=True),
        ),
        migrations.AlterField(
            model_name='area',
            name='therapist',
            field=models.ForeignKey(blank=True, to='manager.Therapist', null=True),
        ),
    ]
