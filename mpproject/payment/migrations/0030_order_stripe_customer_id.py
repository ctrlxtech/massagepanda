# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0029_auto_20150912_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_customer_id',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
