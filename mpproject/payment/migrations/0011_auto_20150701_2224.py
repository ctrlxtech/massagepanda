# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_auto_20150614_1155'),
        ('payment', '0010_auto_20150629_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTherapist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='preferred_gender',
            field=models.CharField(default='Female', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='service_datetime',
            field=models.DateTimeField(default='2015-07-01 09:21'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=10, choices=[(b'0', b'Pending'), (b'1', b'Confirmed'), (b'2', b'Shipped'), (b'3', b'Canceled'), (b'4', b'Refunded')]),
        ),
        migrations.AddField(
            model_name='ordertherapist',
            name='order',
            field=models.ForeignKey(to='payment.Order'),
        ),
        migrations.AddField(
            model_name='ordertherapist',
            name='staff',
            field=models.ForeignKey(to='manager.Staff'),
        ),
    ]
