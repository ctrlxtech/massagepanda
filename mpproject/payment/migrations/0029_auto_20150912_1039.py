# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0028_auto_20150912_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='need_table',
            field=models.BooleanField(),
        ),
    ]
