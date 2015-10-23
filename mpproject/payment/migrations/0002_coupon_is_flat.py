# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_flat',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
