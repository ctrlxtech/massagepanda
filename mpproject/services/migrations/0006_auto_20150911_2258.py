# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20150910_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True),
        ),
    ]
