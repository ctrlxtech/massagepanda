# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_auto_20150702_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.CharField(max_length=1, choices=[(b'1', b'Very Poor'), (b'2', b'Poor'), (b'3', b'OK'), (b'4', b'Good'), (b'5', b'Very Good')])),
                ('comment', models.CharField(max_length=1000)),
                ('order', models.OneToOneField(to='payment.Order')),
            ],
        ),
    ]
