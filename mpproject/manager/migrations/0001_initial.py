# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('areacode', models.CharField(max_length=10, choices=[(b'SF', b'San Francisco'), (b'P', b'Peninsula'), (b'E', b'East Bay'), (b'S', b'South Bay')])),
            ],
        ),
        migrations.CreateModel(
            name='ForwardNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ForwardSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.CharField(max_length=200)),
                ('messageBody', models.CharField(max_length=1000)),
                ('timestamp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='InSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.CharField(max_length=200)),
                ('messageId', models.CharField(max_length=200, null=True)),
                ('messageBody', models.CharField(max_length=1000)),
                ('timestamp', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OutSMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver', models.CharField(max_length=200)),
                ('messageBody', models.CharField(max_length=1000)),
                ('timestamp', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messageBody', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('title', models.PositiveIntegerField()),
                ('phone_number', models.CharField(unique=True, max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('profile_photo', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('phone', models.CharField(unique=True, max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('home_address', models.CharField(max_length=500)),
                ('availability', models.CharField(max_length=500)),
                ('working_area', models.CharField(max_length=500)),
                ('experience', models.CharField(max_length=500)),
                ('specialty', models.CharField(max_length=500)),
                ('massage_license', models.ImageField(upload_to=b'')),
                ('driver_license', models.ImageField(upload_to=b'')),
                ('emergency_contact_name', models.CharField(max_length=50)),
                ('emergency_contact_phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('supplementary', models.CharField(max_length=500, null=True, blank=True)),
                ('rating', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('rate_count', models.PositiveIntegerField(default=0, null=True, blank=True)),
                ('profile_photo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='outsms',
            name='staff',
            field=models.ForeignKey(to='manager.Staff', null=True),
        ),
        migrations.AddField(
            model_name='insms',
            name='staff',
            field=models.ForeignKey(to='manager.Staff', null=True),
        ),
        migrations.AddField(
            model_name='forwardsms',
            name='staff',
            field=models.ForeignKey(to='manager.Staff', null=True),
        ),
        migrations.AddField(
            model_name='forwardnumber',
            name='number',
            field=models.ForeignKey(to='manager.Staff'),
        ),
        migrations.AddField(
            model_name='area',
            name='staff',
            field=models.ForeignKey(blank=True, to='manager.Staff', null=True),
        ),
        migrations.AddField(
            model_name='area',
            name='therapist',
            field=models.ForeignKey(blank=True, to='manager.Therapist', null=True),
        ),
    ]
