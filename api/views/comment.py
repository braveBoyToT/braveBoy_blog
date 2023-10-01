from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from app01.models import Comment, Articles
from django.db.models import F
from api.utils.find_root_comment import find_root_comment

class CommentView(View):

    # 发布评论
    def post(self, request, nid):
        # /api/article/1/comment/
        # 文章id  nid
        # 用户
        # 评论的内容
        res = {
            'msg': '文章评论成功',
            'code': 412,
            'self': None,
        }
        data = request.data
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        content = data.get('content')
        if not content:
            res['msg'] = '请输入评论内容'
            res['self'] = 'content'
            return JsonResponse(res)

        pid = data.get('pid')
        if pid:
            comment_obj = Comment.objects.create(
                content=content,
                user=request.user,
                article=Articles.objects.get(nid=nid),
                parent_comment_id=pid
            )

            # 找到父评论
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') + 1)

            root_comment_obj = find_root_comment(comment_obj)
            if root_comment_obj != Comment.objects.filter(nid=pid).first():
                # 找到最终的根评论
                root_comment_obj.comment_count += 1
                root_comment_obj.save()
        else:
            Comment.objects.create(
                content=content,
                user=request.user,
                article=Articles.objects.get(nid=nid),
            )
        # 添加成功后
        # # 文章评论数加一
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
        res['code'] = 0
        return JsonResponse(res)

    # 删除评论
    def delete(self, request, nid):

        res = {
            'msg': '评论删除失败',
            'code': 412,
        }
        if request.user == Comment.objects.filter(nid=nid).first().user or request.user.is_superuser:
            # 根评论数目减一
            root_comment_obj = find_root_comment(Comment.objects.filter(nid=nid).first())
            root_comment_obj.comment_count -= 1
            root_comment_obj.save()

            # 文章评论数减一
            Comment.objects.filter(nid=nid).first().article.comment_content -=  1
            Comment.objects.filter(nid=nid).first().save()

            Comment.objects.filter(nid=nid).delete()

            res['code'] = 0
            return JsonResponse(res)

        res['msg'] = '用户验证失败'
        return JsonResponse(res)
