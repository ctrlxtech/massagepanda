# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_order_recipient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charge',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='charge',
            name='service',
        ),
        migrations.RemoveField(
            model_name='order',
            name='charged',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='P', max_length=10, choices=[(b'P', b'Pending'), (b'C', b'Confirmed'), (b'S', b'Shipped'), (b'Ca', b'Canceled'), (b'R', b'Refunded')]),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Charge',
        ),
    ]
