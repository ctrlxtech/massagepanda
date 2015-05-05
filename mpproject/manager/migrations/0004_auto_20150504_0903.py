# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20150503_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]
