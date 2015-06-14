# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_auto_20150531_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('areacode', models.CharField(max_length=10, choices=[(b'SF', b'San Francisco'), (b'P', b'Peninsula'), (b'E', b'East Bay'), (b'S', b'South Bay')])),
                ('number', models.ForeignKey(to='manager.Staff')),
            ],
        ),
    ]
