# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20151130_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interval',
            old_name='therapist',
            new_name='schedule',
        ),
    ]
