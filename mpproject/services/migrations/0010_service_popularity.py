# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_serviceimage_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='popularity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
