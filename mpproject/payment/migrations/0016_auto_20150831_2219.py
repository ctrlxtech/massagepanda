# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_auto_20150831_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='preferred_gender',
            field=models.CharField(default=b'0', max_length=10, choices=[(b'0', b'Either'), (b'1', b'Female Preferred'), (b'2', b'Male Preferred')]),
        ),
    ]
