# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0026_order_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='need_table',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='parking_info',
            field=models.CharField(default='whatever', max_length=500),
            preserve_default=False,
        ),
    ]
