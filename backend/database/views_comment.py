from django.views.decorators.http import require_http_methods

from .models import Comment, User, Problem
from .errors import *


def _comment_to_dict(comment: Comment):
    return {
        "id": comment.id,
        "content": comment.content,
        "create_time": comment.created_at,
        "user": {
            "username": comment.user.username,
        }
    }


@require_http_methods(["POST"])
def comment_get_comments_from_id(request):
    parent_id = request.POST.get("parent_id")
    is_sub_comment = request.POST.get("is_sub_comment") == "y"
    # print(f"parent_id: {parent_id}, is_sub_comment: {is_sub_comment}")
    comments = Comment.objects.filter(parent_id=parent_id, is_sub_comment=is_sub_comment)

    return success_data("获取评论成功", [_comment_to_dict(comment) for comment in comments])


@require_http_methods(["POST"])
def comment_add(request):

    username = request.POST.get("username")
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND

    parent_id = request.POST.get("parent_id")
    is_sub_comment = request.POST.get("is_sub_comment") == "y"
    content = request.POST.get("content")

    Comment.objects.create(user=user, parent_id=parent_id, content=content, is_sub_comment=is_sub_comment)

    return success("评论成功")
