# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20150911_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceimage',
            name='service',
            field=models.ForeignKey(related_name='images', default='ffe89482591511e595db0208bb76cfe3', to='services.Service'),
            preserve_default=False,
        ),
    ]
