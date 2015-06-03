# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20150523_1550'),
        ('payment', '0005_order_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='charge',
            old_name='token',
            new_name='charge_token',
        ),
        migrations.AddField(
            model_name='charge',
            name='customer',
            field=models.ForeignKey(default=None, to='customers.Customer', null=True),
        ),
        migrations.AddField(
            model_name='charge',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=None, to='customers.Customer', null=True),
        ),
    ]
