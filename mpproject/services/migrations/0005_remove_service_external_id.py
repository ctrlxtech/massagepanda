# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_service_external_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='external_id',
        ),
    ]
