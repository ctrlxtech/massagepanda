# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='code',
            field=models.CharField(default=1, max_length=40, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feedback',
            name='rated',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='comment',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'Very Poor'), (b'2', b'Poor'), (b'3', b'OK'), (b'4', b'Good'), (b'5', b'Very Good')]),
        ),
    ]
