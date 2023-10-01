import random

from django.views import View
from django.http import JsonResponse
from django import forms
from markdown import markdown  # 解析md
from pyquery import PyQuery  # 解析html
from app01.models import Tags, Articles, Cover
from api.views.login import clean_form


# 添加或修改文章的验证
class AddAriticleform(forms.Form):
    title = forms.CharField(error_messages={'required':'请输入文章标题'})
    content = forms.CharField(error_messages={ 'required':'请输入文章内容'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    # 全局钩子，校验分类和密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')


        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')


    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 获取正文前30个字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:30]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        # 如果没有设置，那就默认
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id

# 给文章添加标签
def add_article_tags(article_obj, tags):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)

class ArticleView(View):

# 发布文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None,
        }
        data = request.data
        data['status'] = 1
        form = AddAriticleform(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = 'Zccc'
        form.cleaned_data['source'] = 'braveBoy个人博客'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tags(article_obj, tags)

        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)


# 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功',
            'code': 412,
            'data': None,
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)

        data = request.data
        data['status'] = 1

        form = AddAriticleform(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = 'Zccc'
        form.cleaned_data['source'] = 'braveBoy个人博客'
        article_query.update(**form.cleaned_data)

        # 标签修改
        # # 先清空原标签
        tags = data.get('tags')
        article_query.first().tag.clear()
        # 添加标签
        add_article_tags(article_query.first(), tags)

        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)







# # 文章
# class ArticleView(View):
#     # 发布文章
#     def post(self, request):
#         res = {
#             'msg': '文章发布成功',
#             'code': 412,
#             'data': None,
#         }
#         data: dict = request.data
#
#         title = data.get('title')
#         if not title:
#             res['msg'] = '请输入文章标题'
#             return JsonResponse(res)
#
#         content = data.get('content')
#         if not content:
#             res['msg'] = '请输入文章内容'
#             return JsonResponse(res)
#
#         extra = {
#             'title': title,
#             'content': content,
#             'status': 1,
#         }
#
#         # # 将 markdown 解析为 html
#         # doc = markdown(content)
#         # # 将 html 解析成文本
#         # doc = PyQuery(doc).text()
#         # doc = PyQuery((markdown(content))).text()
#
#         abstract = data.get('abstract')
#         if not abstract:
#             abstract = PyQuery((markdown(content))).text()[:30]
#         extra['abstract'] = abstract
#
#         category = data.get('categorr')
#         if category:
#             extra['category'] = category
#
#         cover_id = data.get('cover_id')
#         if cover_id:
#             extra['cover_id'] = cover_id
#         else:
#             extra['cover_id'] = 1
#
#         pwd = data.get('pwd')
#         if category:
#             extra['pwd'] = pwd
#
#         # 创建文章对象
#         article_obj = Articles.objects.create(**extra)
#
#         # 标签
#         tags = data.get('tags')
#         if tags:
#             for tag in tags:
#                 if not tag.isdigit():
#                     tag_obj = Tags.objects.create(title=tag)
#                     article_obj.tag.add(tag_obj)
#                 else:
#                     article_obj.tag.add(tag)
#         res['code'] = 0
#         res['data'] = article_obj.nid
#         return JsonResponse(res)

