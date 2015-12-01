# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_auto_20151130_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='areacode',
            field=models.CharField(max_length=10, choices=[(b'0', b'San Francisco'), (b'1', b'Peninsula'), (b'2', b'East Bay'), (b'3', b'South Bay')]),
        ),
    ]
