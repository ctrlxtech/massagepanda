# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20150911_2258'),
        ('payment', '0025_remove_order_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(default=None, to='services.Service', null=True),
        ),
    ]
