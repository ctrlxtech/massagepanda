# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_coupon_is_gilt'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='labor_adjustment',
            field=models.IntegerField(default=0),
        ),
    ]
