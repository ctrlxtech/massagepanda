# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_customercredit'),
        ('referral', '0002_auto_20151016_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerreferralhistory',
            name='referred_customer',
            field=models.OneToOneField(default=1, to='customers.Customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customerreferralhistory',
            name='status',
            field=models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pending'), (b'S', b'Success'), (b'C', b'Cancelled')]),
        ),
    ]
