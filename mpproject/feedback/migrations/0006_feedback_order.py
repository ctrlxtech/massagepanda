# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0023_ordertherapist_order'),
        ('feedback', '0005_remove_feedback_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='order',
            field=models.OneToOneField(default=1, to='payment.Order'),
            preserve_default=False,
        ),
    ]
