# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_therapist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='therapist',
            old_name='Supplementary',
            new_name='supplementary',
        ),
        migrations.AddField(
            model_name='therapist',
            name='emergency_contact_phone',
            field=models.CharField(default=412, max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='therapist',
            name='gender',
            field=models.CharField(default=1, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')]),
            preserve_default=False,
        ),
    ]
