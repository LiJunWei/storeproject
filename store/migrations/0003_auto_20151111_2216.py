# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20151111_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caritem',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='数量'),
        ),
    ]
