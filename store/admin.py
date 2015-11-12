# coding: utf-8
from django.contrib import admin
from store.models import *

class ClothingAdmin(admin.ModelAdmin):
    list_display = ('brand','name','num',)
    fieldsets = (
        ('None',{'fields':('category','name','brand','size','old_price',
                           'new_price','desc','sales','tag','num','image_url_i',
                           'image_url_l','image_url_m','image_url_r','image_url_c',)}),
    )
admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Clothing,ClothingAdmin)