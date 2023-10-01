def find_root_comment(comment):
    # 找comment的最终根评论
    if comment.parent_comment:
        return find_root_comment(comment.parent_comment)
    return comment