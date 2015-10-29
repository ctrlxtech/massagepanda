# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_labor_cost'),
        ('payment', '0003_auto_20151025_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCoupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='coupon',
            name='quantity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicecoupon',
            name='coupon',
            field=models.ForeignKey(to='payment.Coupon'),
        ),
        migrations.AddField(
            model_name='servicecoupon',
            name='service',
            field=models.ForeignKey(to='services.Service'),
        ),
    ]
