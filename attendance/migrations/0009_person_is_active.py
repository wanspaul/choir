# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0008_auto_20160416_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
