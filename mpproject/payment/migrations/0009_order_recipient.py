# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_auto_20150628_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='recipient',
            field=models.CharField(default='Kevin', max_length=50),
            preserve_default=False,
        ),
    ]
