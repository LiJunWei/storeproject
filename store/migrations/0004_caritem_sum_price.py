# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20151111_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='caritem',
            name='sum_price',
            field=models.FloatField(default=0, verbose_name='小计'),
        ),
    ]
