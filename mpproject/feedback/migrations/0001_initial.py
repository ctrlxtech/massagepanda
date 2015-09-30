# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'Very Poor'), (b'2', b'Poor'), (b'3', b'OK'), (b'4', b'Good'), (b'5', b'Very Good')])),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
                ('code', models.UUIDField(default=uuid.uuid1, unique=True, editable=False, db_index=True)),
                ('request_count', models.DecimalField(default=0, max_digits=1, decimal_places=0)),
                ('rated', models.BooleanField()),
                ('order', models.OneToOneField(to='payment.Order')),
            ],
        ),
    ]
