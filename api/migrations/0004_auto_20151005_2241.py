# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151005_2238'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='key',
            unique_together=set([('user', 'name')]),
        ),
    ]
