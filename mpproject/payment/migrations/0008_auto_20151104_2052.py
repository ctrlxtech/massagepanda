# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 4, 52, 36, 7110, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 5, 4, 52, 43, 215055, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
