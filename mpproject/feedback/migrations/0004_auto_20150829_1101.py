# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_feedback_request_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='code',
            field=models.CharField(unique=True, max_length=40, db_index=True),
        ),
    ]
