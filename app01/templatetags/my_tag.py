from django import template

# 注册
register = template.Library()

# 自定义过滤器
# @register.filter()
# def add1(item):
#     return int(item) + 1

@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    img_list = [
        "/static/my/img/jay/jay_00.jpg",
        "/static/my/img/jay/jay_06.jpg",
        "/static/my/img/jay/jay_07.jpg",
    ]
    return {"img_list": img_list}