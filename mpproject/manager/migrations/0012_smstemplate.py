# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_auto_20150512_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messageBody', models.CharField(max_length=1000)),
            ],
        ),
    ]
