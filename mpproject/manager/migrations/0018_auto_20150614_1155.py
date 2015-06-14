# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_auto_20150608_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='insms',
            name='staff',
            field=models.ForeignKey(to='manager.Staff', null=True),
        ),
        migrations.AddField(
            model_name='outsms',
            name='staff',
            field=models.ForeignKey(to='manager.Staff', null=True),
        ),
    ]
