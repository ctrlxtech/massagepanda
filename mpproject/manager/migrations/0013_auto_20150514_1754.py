# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0012_smstemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='title',
            field=models.PositiveIntegerField(),
        ),
    ]
