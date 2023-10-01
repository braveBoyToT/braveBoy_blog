import os

"""根据根评论递归查找子评论"""

# 加载django项目的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "braveBoy_blog.settings")
# 导入Django，并启动django项目
import django

django.setup()
from app01.models import Articles, Comment


def find_root_sub_comment(root_comment: Comment, sub_comment_list):
    if root_comment.comment_set.all():
        for sub_comment in root_comment.comment_set.all():
            sub_comment_list.append(sub_comment)
            find_root_sub_comment(sub_comment, sub_comment_list)

def sub_comment_list(nid):
    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=nid).order_by('-create_time')
    comment_list = []
    # print(comment_query)
    for comment in comment_query:
        if not comment.parent_comment:
            # 找到所有的根评论并存入字典
            comment_list.append(comment)
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            continue
    return comment_list
