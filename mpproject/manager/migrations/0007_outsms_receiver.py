# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_outsms'),
    ]

    operations = [
        migrations.AddField(
            model_name='outsms',
            name='receiver',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
