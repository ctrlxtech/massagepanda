# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0022_auto_20150911_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertherapist',
            name='order',
            field=models.ForeignKey(default=1, to='payment.Order'),
            preserve_default=False,
        ),
    ]
