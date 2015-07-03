# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_auto_20150620_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default='paul', max_length=45, verbose_name=b'Name'),
            preserve_default=False,
        ),
    ]
