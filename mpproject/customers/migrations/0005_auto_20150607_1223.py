# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_customer_stripe_customer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state_province',
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=40, verbose_name=b'State', blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='zipcode',
            field=models.CharField(default=1, max_length=10, verbose_name=b'Zip Code'),
            preserve_default=False,
        ),
    ]
