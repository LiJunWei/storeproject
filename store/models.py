# coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
import json

#用户
class User(AbstractUser):
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

#广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title

#分类
class Category(models.Model):
    typ = models.CharField(max_length=20, verbose_name='所属大类')
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=1,verbose_name='分类的排序')
    #0代表男性，1代表女性
    sex = models.IntegerField(default=0,verbose_name='性别')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __str__(self):
        str = "男" if self.sex == 0 else "女"
        return self.name + "---" + str

#品牌
class Brand(models.Model):
    name = models.CharField(max_length=30, verbose_name='品牌名称')
    index = models.IntegerField(default=1,verbose_name='排列顺序')

    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name

#尺寸
class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name='尺寸')
    index = models.IntegerField(default=1, verbose_name='排列顺序')

    class Meta:
        verbose_name = '尺寸'
        verbose_name_plural = verbose_name
        ordering = ['index',]

    def __str__(self):
        return self.name

#标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#商品包括衣服鞋子等
class Clothing(models.Model):
    category = models.ForeignKey(Category, verbose_name='分类')
    name = models.CharField(max_length=30, verbose_name='名称')
    brand = models.ForeignKey(Brand, verbose_name='品牌')
    size = models.ManyToManyField(Size, verbose_name='尺寸')
    old_price = models.FloatField(default=0.0, verbose_name='原价')
    new_price = models.FloatField(default=0.0, verbose_name='现价')
    discount = models.FloatField(default=1, verbose_name='折扣')
    desc = models.CharField(max_length=100, verbose_name='简介')
    sales = models.IntegerField(default=0, verbose_name='销量')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    num = models.IntegerField(default=0, verbose_name='库存')
    image_url_i = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='展示图片路径')
    image_url_l = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='详情图片路径1')
    image_url_m = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='详情图片路径2')
    image_url_r = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/default.jpg', verbose_name='详情图片路径3')
    image_url_c = models.ImageField(upload_to='clothing/%Y/%m', default= 'clothing/ce.jpg', verbose_name='购物车展示图片')

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.brand.name + "---" + self.category.name

#购物车条目
class Caritem(models.Model):
    clothing = models.ForeignKey(Clothing, verbose_name='购物车中产品条目')
    quantity = models.IntegerField(default=0, verbose_name='数量')
    sum_price = models.FloatField(default=0.0, verbose_name='小计')

    class Meta:
        verbose_name = '购物车条目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

#购物车
class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0.0

    def add(self, clothing):
        self.total_price += clothing.new_price
        for item in self.items:
            if item.clothing.id == clothing.id:
                item.quantity += 1
                item.sum_price += clothing.new_price
                return
        else:
            self.items.append(Caritem(clothing=clothing, quantity=1, sum_price=clothing.new_price))



