# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_auto_20151101_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 3, 19, 47, 37, 412609, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
