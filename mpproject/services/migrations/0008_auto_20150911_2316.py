# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_remove_serviceimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceimage',
            name='service',
        ),
        migrations.AddField(
            model_name='serviceimage',
            name='image',
            field=models.ImageField(default=1, upload_to=b''),
            preserve_default=False,
        ),
    ]
