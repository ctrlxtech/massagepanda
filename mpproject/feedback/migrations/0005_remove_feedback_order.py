# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20150829_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='order',
        ),
    ]
