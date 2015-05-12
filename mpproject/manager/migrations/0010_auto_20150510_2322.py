# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_auto_20150510_2312'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ForwordNumber',
            new_name='ForwardNumber',
        ),
    ]
