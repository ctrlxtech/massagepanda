# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_auto_20150807_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.EmailField(default='yuechen1989@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(default=14128889022, max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
            preserve_default=False,
        ),
    ]
