from django.contrib import admin
from app01.models import Articles  # 文章表
from app01.models import Tags  # 标签表
from app01.models import Cover  # 封面表
from app01.models import Comment  # 评论表
from app01.models import Avatars  # 头像表
from app01.models import UserInfo  # 用户表


# Register your models here.

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)



