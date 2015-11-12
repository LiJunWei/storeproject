# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caritem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(verbose_name='数量', default=1)),
            ],
            options={
                'verbose_name_plural': '购物车条目',
                'verbose_name': '购物车条目',
            },
        ),
        migrations.AddField(
            model_name='clothing',
            name='image_url_c',
            field=models.ImageField(verbose_name='购物车展示图片', upload_to='clothing/%Y/%m', default='clothing/ce.jpg'),
        ),
        migrations.AddField(
            model_name='caritem',
            name='clothing',
            field=models.ForeignKey(verbose_name='购物车中产品条目', to='store.Clothing'),
        ),
    ]
