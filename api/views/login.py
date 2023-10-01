from django.contrib import auth
from django import forms
from app01.models import UserInfo, Avatars
from django.views import  View
from django.http import JsonResponse
import random
class LoginBaseForm(forms.Form):
    # 重写init方法
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # woc这个pop太nb了将其弹出，避免了父类中没有该变量的错误，太牛逼了

        super().__init__(*args, **kwargs)

    # 配置局部钩子
    def clean_code(self):
        code:str = self.cleaned_data.get('code')
        valid_code:str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码输入错误')
        return self.cleaned_data

# 登录的字段验证
class LoginForm(LoginBaseForm):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    # 配置全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')

        user = auth.authenticate(username=name, password=pwd)

        # 检查用户名和密码是否填写正确
        if not user:
            #  为错误的字段添加错误信息
            self.add_error('name', '用户名或密码错误')
            return self.cleaned_data

        # 将用户对象存入到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data

# 注册字段验证
class SignForm(LoginBaseForm):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    re_pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '该用户名已注册')
        return self.cleaned_data

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data


# CBV

# 登录字段未输入完全的可复用代码
def clean_form(form):
    err_dict: dict = form.errors
    # 拿到所有空缺字段的名字
    err_valid = list(err_dict.keys())[0]
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg

class LoginView(View):
    def post(self,request):
        res = {
            'code': 1,
            'msg': "登陆成功",
            'self': None
        }
        data = request.data  # 解析出来就是python中的字典////由于每次请求都会需要到这个loads，所以我们可以将该部分放到django的中间件中，使其自动解析

        form = LoginForm(data, request = request)

        # 检查loginform中传出来的所有登录字段的合法情况
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 编写在验证过密码后的 登录操作
        user = form.cleaned_data.get('user')
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)

class SignView(View):
    def post(self,request):
        res = {
            'code': 1,
            'msg': "注册成功",
            'self': None
        }
        form = SignForm(request.data, request = request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 注册成功后的代码
        # # 在表中增加数据
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd'),
        )

        # 随机选择头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.save()
        # # 注册后直接登录
        auth.login(request, user)
        res['code'] = 0

        return JsonResponse(res)



