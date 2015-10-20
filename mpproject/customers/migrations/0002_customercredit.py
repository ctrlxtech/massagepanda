# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('customer', models.OneToOneField(to='customers.Customer')),
            ],
        ),
    ]
