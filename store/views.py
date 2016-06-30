# coding: utf-8
from django.shortcuts import render,redirect
from store.models import *
from django.conf import settings
import logging
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from store.forms import *
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import F

logger = logging.getLogger('store.views')

def authenticated_view(function):
  def wrap(request, *args, **kwargs):
      if request.user.is_authenticated():
          return function(request)
      else:
        login_form = LoginForm()
        return render(request, 'login.html', locals())

  wrap.__doc__=function.__doc__
  wrap.__name__=function.__name__
  return wrap

def global_setting(request):
    #站点信息
    MEDIA_URL = settings.MEDIA_URL
    category_list = Category.objects.all()
    #男装分类信息
    category_list_m = [c for c in category_list if c.sex == 0]
    #女装分类信息
    category_list_f = [c for c in category_list if c.sex == 1]
    #品牌信息
    brand_list = Brand.objects.all()
    #热销榜
    hot_list = Clothing.objects.all().order_by('-sales')[:4]
    #标签
    tag_list = Tag.objects.all()
    #购物车
    cart = request.session.get(request.user.id, None)
    return locals()

#主页
def index(request):
    ad_list = Ad.objects.all()
    clo_list = Clothing.objects.all()
    clo_list = getPage(request,clo_list)
    return render(request,"index.html",locals())

#产品列表页
def products(request):
    try:
        cid = request.GET.get('cid',None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'error.html', {"reason":"分类不存在"})
        clo_list = Clothing.objects.filter(category=category)
        clo_list = getPage(request,clo_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'products.html', locals())

#标签列表页
def tags(request):
    try:
        tid = request.GET.get('tid',None)
        try:
            tag = Tag.objects.get(pk=tid)
        except Tag.DoesNotExist:
            return render(request, 'error.html', {"reason":"标签不存在"})
        clo_list = Clothing.objects.filter(tag=tag)
        clo_list = getPage(request,clo_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'products.html', locals())

#商品详情页
def detail(request):
    try:
        did = request.GET.get('did', None)
        try:
            clo = Clothing.objects.get(pk=did)
        except Clothing.DoesNotExist:
            return render(request, 'error.html', {"reason":"商品不存在"})
    except Exception as e:
        logger.error(e)
    return render(request, 'single.html', locals())

#品牌列表页
def brands(request):
    try:
        bid = request.GET.get('bid',None)
        try:
            brand = Brand.objects.get(pk=bid)
        except Brand.DoesNotExist:
            return render(request, 'error.html', {"reason":"品牌不存在"})
        clo_list = Clothing.objects.filter(brand=brand)
        clo_list = getPage(request,clo_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'products.html', locals())

#注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request,'error.html',{'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request,'register.html',locals())

#登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username,password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request,'error.html',{'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'error.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

#退出
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    login_form = LoginForm()
    return render(request, 'login.html', locals())

#查看购物车
@authenticated_view
def view_cart(request):
    cart = request.session.get(request.user.id, None)
    return render(request, 'checkout.html', locals())

#添加购物车
@authenticated_view
def add_cart(request):
    try:
        chid = request.POST.get('chid',None)
        try:
            clothing = Clothing.objects.get(pk=chid)
        except Clothing.DoesNotExist:
            return render(request, 'error.html', {'reason':'商品不存在'})
        cart = request.session.get(request.user.id,None)
        if not cart:
            cart = Cart()
            cart.add(clothing)
            request.session[request.user.id] = cart
        else:
            cart.add(clothing)
            request.session[request.user.id] = cart
    except Exception as e:
        logger.error(e)
    return render(request, 'checkout.html', locals())

#清空购物车
@authenticated_view
def cleanCart(request):
    cart = Cart()
    request.session[request.user.id] = cart
    return render(request, 'checkout.html', locals())

@authenticated_view
def clean_one_item(request, id):
    item = None
    try:
     item = Clothing.objects.get(pk=id)
    except Clothing.DoesNotExist:
        pass
    if item:
        item.delete()
    cart = request.session.get(request.user.id, None)
    return render(request, 'checkout.html', {'cart':cart})

#打折商品
def getDiscount(request):
    try:
        clo_list = Clothing.objects.filter(new_price__lt=F('old_price'))
        clo_list = getPage(request,clo_list)
        logger.debug("len clo_list:%d", len(clo_list))
        discount = True
    except Exception as e:
        logger.error(e)
    return render(request, 'products.html', locals())


#分页
def getPage(request,clo_list):
    paginator = Paginator(clo_list,8)
    try:
        page = int(request.GET.get('page',1))
        clo_list = paginator.page(page)
    except (EmptyPage,InvalidPage,PageNotAnInteger):
        clo_list = paginator.page(1)
    return clo_list
