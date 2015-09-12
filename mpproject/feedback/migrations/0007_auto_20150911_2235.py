# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_feedback_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='code',
            field=models.UUIDField(default=uuid.uuid1, unique=True, editable=False, db_index=True),
        ),
    ]
