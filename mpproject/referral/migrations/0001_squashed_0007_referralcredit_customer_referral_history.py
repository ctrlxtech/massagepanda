# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    replaces = [(b'referral', '0001_initial'), (b'referral', '0002_auto_20151016_2140'), (b'referral', '0003_auto_20151016_2216'), (b'referral', '0004_referralcredit'), (b'referral', '0005_auto_20151119_2137'), (b'referral', '0006_remove_referralcredit_customer_referral_history'), (b'referral', '0007_referralcredit_customer_referral_history')]

    dependencies = [
        ('payment', '0001_initial'),
        ('customers', '0001_initial'),
        ('customers', '0002_customercredit'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerReferralCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=80)),
                ('customer', models.OneToOneField(to='customers.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerReferralHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pending'), (b'S', b'Success'), (b'C', b'Cancelled')])),
                ('code', models.ForeignKey(to='referral.CustomerReferralCode')),
                ('order', models.OneToOneField(null=True, blank=True, to='payment.Order')),
                ('referred_customer', models.OneToOneField(default=1, to='customers.Customer')),
            ],
        ),
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
        migrations.CreateModel(
            name='ReferralCredit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('credit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('accumulative_credit', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('customer', models.ForeignKey(to='customers.Customer')),
                ('customer_referral_history', models.ForeignKey(default=1, to='referral.CustomerReferralHistory')),
            ],
        ),
    ]
