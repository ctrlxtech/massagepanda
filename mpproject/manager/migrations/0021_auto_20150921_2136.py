# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0020_auto_20150816_0020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='rate',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='rate_count',
        ),
        migrations.AddField(
            model_name='therapist',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
    ]
