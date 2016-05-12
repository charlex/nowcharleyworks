# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nowcharleyworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
