# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_coupon_is_flat'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(default=None, blank=True, to='payment.Coupon', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'0', max_length=10, choices=[(b'0', b'Pending'), (b'1', b'Confirmed'), (b'2', b'Shipped'), (b'3', b'Canceled'), (b'4', b'Charged'), (b'5', b'Refunded'), (b'6', b'Charged10'), (b'7', b'Charged40')]),
        ),
    ]
