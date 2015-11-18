# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customercredit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line2',
            field=models.CharField(max_length=45, null=True, verbose_name=b'Address line 2', blank=True),
        ),
    ]
