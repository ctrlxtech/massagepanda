# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
        ('payment', '0006_auto_20150524_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='service',
            field=models.ForeignKey(default=None, to='services.Service', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(default=None, to='services.Service', null=True),
        ),
    ]
