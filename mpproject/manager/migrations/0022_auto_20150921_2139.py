# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0021_auto_20150921_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='therapist',
            old_name='rate',
            new_name='rating',
        ),
    ]
