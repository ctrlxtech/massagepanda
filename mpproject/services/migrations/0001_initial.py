# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('service_type', models.CharField(max_length=200)),
                ('service_detail', models.CharField(max_length=200)),
                ('service_time', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('service_sale', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('service_fee', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('popularity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('service', models.ForeignKey(related_name='images', to='services.Service')),
            ],
        ),
    ]
