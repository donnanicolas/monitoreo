# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150907_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='key',
            name='key',
            field=models.CharField(default=api.models.generate_key, unique=True, max_length=32),
        ),
    ]
