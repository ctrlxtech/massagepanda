# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_auto_20150614_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForwardSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.CharField(max_length=200)),
                ('messageBody', models.CharField(max_length=1000)),
                ('timestamp', models.CharField(max_length=200)),
                ('staff', models.ForeignKey(to='manager.Staff', null=True)),
            ],
        ),
    ]
