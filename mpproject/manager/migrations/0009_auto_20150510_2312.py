# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20150510_2311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forwordnumber',
            old_name='numberKey',
            new_name='number',
        ),
    ]
