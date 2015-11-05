# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_coupon_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='used',
            field=models.IntegerField(default=0),
        ),
    ]
