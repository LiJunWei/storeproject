# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, max_length=30, error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=254)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('qq', models.CharField(blank=True, verbose_name='QQ号码', max_length=20, null=True)),
                ('mobile', models.CharField(blank=True, unique=True, verbose_name='手机号码', max_length=11, null=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_name='user_set', help_text='Specific permissions for this user.', blank=True, related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户',
                'ordering': ['-id'],
                'verbose_name_plural': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(verbose_name='标题', max_length=50)),
                ('image_url', models.ImageField(verbose_name='图片路径', upload_to='ad/%Y/%m')),
                ('date_publish', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
                ('index', models.IntegerField(default=1, verbose_name='排列顺序')),
            ],
            options={
                'verbose_name': '广告',
                'ordering': ['index', 'id'],
                'verbose_name_plural': '广告',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='品牌名称', max_length=30)),
                ('index', models.IntegerField(default=1, verbose_name='排列顺序')),
            ],
            options={
                'verbose_name': '品牌',
                'ordering': ['index'],
                'verbose_name_plural': '品牌',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('typ', models.CharField(verbose_name='所属大类', max_length=20)),
                ('name', models.CharField(verbose_name='分类名称', max_length=30)),
                ('index', models.IntegerField(default=1, verbose_name='分类的排序')),
                ('sex', models.IntegerField(default=0, verbose_name='性别')),
            ],
            options={
                'verbose_name': '分类',
                'ordering': ['index', 'id'],
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Clothing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='名称', max_length=30)),
                ('old_price', models.FloatField(default=0.0, verbose_name='原价')),
                ('new_price', models.FloatField(default=0.0, verbose_name='现价')),
                ('discount', models.FloatField(default=1, verbose_name='折扣')),
                ('desc', models.CharField(verbose_name='简介', max_length=100)),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('num', models.IntegerField(default=0, verbose_name='库存')),
                ('image_url_i', models.ImageField(default='clothing/default.jpg', verbose_name='展示图片路径', upload_to='clothing/%Y/%m')),
                ('image_url_l', models.ImageField(default='clothing/default.jpg', verbose_name='详情图片路径1', upload_to='clothing/%Y/%m')),
                ('image_url_m', models.ImageField(default='clothing/default.jpg', verbose_name='详情图片路径2', upload_to='clothing/%Y/%m')),
                ('image_url_r', models.ImageField(default='clothing/default.jpg', verbose_name='详情图片路径3', upload_to='clothing/%Y/%m')),
                ('brand', models.ForeignKey(verbose_name='品牌', to='store.Brand')),
                ('category', models.ForeignKey(verbose_name='分类', to='store.Category')),
            ],
            options={
                'verbose_name': '商品',
                'ordering': ['id'],
                'verbose_name_plural': '商品',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='尺寸', max_length=20)),
                ('index', models.IntegerField(default=1, verbose_name='排列顺序')),
            ],
            options={
                'verbose_name': '尺寸',
                'ordering': ['index'],
                'verbose_name_plural': '尺寸',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='标签', max_length=30)),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='clothing',
            name='size',
            field=models.ManyToManyField(verbose_name='尺寸', to='store.Size'),
        ),
        migrations.AddField(
            model_name='clothing',
            name='tag',
            field=models.ManyToManyField(verbose_name='标签', to='store.Tag'),
        ),
    ]
