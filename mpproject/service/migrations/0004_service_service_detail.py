# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20150416_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_detail',
            field=models.CharField(default='coming soon', max_length=200),
            preserve_default=False,
        ),
    ]
