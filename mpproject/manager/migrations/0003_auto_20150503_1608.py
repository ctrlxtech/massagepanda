# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_staff_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='staff',
            name='last_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
