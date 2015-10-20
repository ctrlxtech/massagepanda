# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferredCustomer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('redeemed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='customerreferralcode',
            name='code',
            field=models.CharField(max_length=80, db_index=True),
        ),
        migrations.AddField(
            model_name='referredcustomer',
            name='code',
            field=models.ForeignKey(to='referral.CustomerReferralCode'),
        ),
        migrations.AddField(
            model_name='referredcustomer',
            name='customer',
            field=models.OneToOneField(to='customers.Customer'),
        ),
    ]
