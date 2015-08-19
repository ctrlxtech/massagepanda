# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerreferralhistory',
            name='referral',
        ),
        migrations.AlterField(
            model_name='customerreferralhistory',
            name='order',
            field=models.OneToOneField(to='payment.Order'),
        ),
    ]
