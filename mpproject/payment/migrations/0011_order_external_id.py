# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_order_credit_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='external_id',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
