# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0030_order_stripe_customer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='stripe_customer_id',
        ),
    ]
