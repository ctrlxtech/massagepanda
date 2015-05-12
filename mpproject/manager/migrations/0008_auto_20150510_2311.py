# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_outsms_receiver'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForwordNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='staff',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='forwordnumber',
            name='numberKey',
            field=models.ForeignKey(to='manager.Staff'),
        ),
    ]
