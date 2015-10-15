# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20151011_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='active',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
