# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0013_auto_20150514_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('phone', models.CharField(unique=True, max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('home_address', models.CharField(max_length=500)),
                ('availability', models.CharField(max_length=500)),
                ('working_area', models.CharField(max_length=500)),
                ('experience', models.CharField(max_length=500)),
                ('specialty', models.CharField(max_length=500)),
                ('massage_license', models.ImageField(upload_to=b'')),
                ('driver_license', models.ImageField(upload_to=b'')),
                ('emergency_contact_name', models.CharField(max_length=50)),
                ('Supplementary', models.CharField(max_length=500, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
