# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20150911_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceimage',
            name='image',
        ),
    ]
