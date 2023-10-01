from django.utils.deprecation import MiddlewareMixin
import json #解析json字符串

# 解析post请求的数据
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method != "get" and request.META.get('CONTENT_TYPE') == 'application/json':
            # 后一个and是解决加了这个中间件后登录django自带的后台报错的问题
            request.data = json.loads(request.body)  # axios传递的字符串变量存储在请求体中而不是post中
            # 并且该版本二点loads没有encoding参数


    # 响应中间件
    def process_response(self, request, response):

        return response