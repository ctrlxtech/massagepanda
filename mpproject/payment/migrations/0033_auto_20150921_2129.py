# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0020_auto_20150816_0020'),
        ('payment', '0032_auto_20150919_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordertherapist',
            name='staff',
        ),
        migrations.AddField(
            model_name='ordertherapist',
            name='therapist',
            field=models.ForeignKey(default=1, to='manager.Therapist'),
            preserve_default=False,
        ),
    ]
