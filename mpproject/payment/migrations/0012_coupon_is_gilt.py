# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_order_external_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_gilt',
            field=models.BooleanField(default=False),
        ),
    ]
