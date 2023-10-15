from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse  # 用于返回对象
from app01.utils.random_code import random_code
from app01.utils.sub_comment import sub_comment_list
from django import forms
from django.contrib import auth
from app01.models import UserInfo
from app01.models import Articles, Tags, Cover

# Create your views here.
def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')
    frontend_list = article_list.filter(category='1')[:6]
    backend_list = article_list.filter(category='2')[:6]
    return render(request,'index.html', locals())

def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    if not article_query:
        return redirect('/')
    article_obj = article_query.first()
    comment_list = sub_comment_list(nid = nid)
    return render(request, 'article.html', locals())

def news(request):

    return render(request,'news.html')

def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)

def login(request):

    return render(request,'login.html')

def sign(request):

    return render(request,'sign.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def backend(request):
    # 若没有登录就进入这个路由
    if not request.user.username:
        return redirect('/')
    return render(request, 'backend/backend.html', locals())

def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html', locals())

def add_article(request):
    # 拿到所有的文章类型
    category_list = Articles.category_choice
    # 拿到所有的分类标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
    })
    return render(request, 'backend/add_article.html', locals())

def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())

def edit_article(request, nid):
    # 拿到所有的文章类型
    category_list = Articles.category_choice
    # 拿到所有的分类标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
    })
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]

    return render(request, 'backend/edit_article.html', locals())

