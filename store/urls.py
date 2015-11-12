from django.conf.urls import include, url
from store.views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^products/$', products, name='products'),
    url(r'^tags/$', tags, name='tags'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^register/$', do_reg, name='register'),
    url(r'^login/$', do_login, name='login'),
    url(r'^logout/$', do_logout, name='logout'),
    url(r'^view_cart/$', view_cart, name='view_cart'),
    url(r'^add_cart/$', add_cart, name='add_cart'),
    url(r'^clean_cart/$', cleanCart, name='clean_cart'),
    url(r'^brands/$', brands, name='brands'),
    url(r'discount/$', getDiscount, name='discount')
]
