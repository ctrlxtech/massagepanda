# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_auto_20160103_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='areacode',
            field=models.CharField(max_length=10, choices=[(b'0', b'San Francisco'), (b'1', b'Peninsula'), (b'2', b'East Bay'), (b'3', b'South Bay'), (b'10', b'Chicago')]),
        ),
    ]
