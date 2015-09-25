# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0023_auto_20150921_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='therapist',
            field=models.ForeignKey(default=1, to='manager.Therapist'),
            preserve_default=False,
        ),
    ]
