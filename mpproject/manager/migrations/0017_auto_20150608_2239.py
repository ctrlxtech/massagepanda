# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0016_area'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='number',
            new_name='staff',
        ),
    ]
