import os

"""根据子评论递归查找他的根评论"""

if __name__ == "__main__":
    # 加载django项目的配置信息
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "braveBoy_blog.settings")
    # 导入Django，并启动django项目
    import django
    django.setup()
    from app01.models import Articles, Comment

    def find_root_comment(comment: Comment):
        # 找到comment的最终根评论
        if comment.parent_comment:
            # 如果进来了就说明不是根评论
            return find_root_comment(comment.parent_comment)
        # 是根评论就返回
        return comment


    comment_dict = {}
    # 找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=22)
    for comment in comment_query:
        if not comment.parent_comment:
            # 找到所有的根评论并存入字典
            comment.sub_comment = []
            comment_dict[comment.nid] = comment
    for comment in comment_query:
        # 遍历该评论下的所有子评论
        for sub_comment in comment.comment_set.all():
            root_comment = find_root_comment(sub_comment)
            comment_dict[root_comment.nid].sub_comment.append(sub_comment)

    for k,v in comment_dict.items():
        print(v)
        for comment in v.sub_comment:
            print(' ',comment)