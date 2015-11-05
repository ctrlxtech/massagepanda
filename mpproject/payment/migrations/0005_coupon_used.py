# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20151027_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='used',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
