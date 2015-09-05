# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_auto_20150830_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='token',
            new_name='stripe_token',
        ),
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(default=1, max_length=40, db_index=True),
            preserve_default=False,
        ),
    ]
