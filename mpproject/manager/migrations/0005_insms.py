# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20150504_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='InSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.CharField(max_length=200)),
                ('messageId', models.CharField(max_length=200, null=True)),
                ('messageBody', models.CharField(max_length=1000)),
                ('timestamp', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
