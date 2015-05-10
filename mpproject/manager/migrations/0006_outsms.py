# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_insms'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messageBody', models.CharField(max_length=1000)),
                ('timestamp', models.CharField(max_length=200)),
            ],
        ),
    ]
