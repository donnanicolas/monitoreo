# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='key',
            name='create_at',
        ),
        migrations.AddField(
            model_name='key',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='key',
            name='key',
            field=models.CharField(default=api.models.generate_key, max_length=512),
        ),
    ]
