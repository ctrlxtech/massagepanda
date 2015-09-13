# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0024_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='service',
        ),
    ]
