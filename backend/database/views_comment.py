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
def comment_get_comments_from_problem(request):
    problem_id = request.POST.get("problem_id")
    # 找到对应 problem
    problem = Problem.objects.get(id=problem_id)
    if not problem:
        return E_PROBLEM_NOT_FIND

    comments = Comment.objects.filter(problem=problem)
    return success_data("获取评论成功", [_comment_to_dict(comment) for comment in comments])


@require_http_methods(["POST"])
def comment_add(request):
    problem_id = request.POST.get("problem_id")
    problem = Problem.objects.get(id=problem_id)
    if not problem:
        return E_PROBLEM_NOT_FIND

    username = request.POST.get("username")
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND

    comment_id_to_reply = request.POST.get("comment_id_to_reply")
    parent = Comment.objects.get(id=comment_id_to_reply) if comment_id_to_reply else None

    content = request.POST.get("content")
    Comment.objects.create(problem=problem, user=user, content=content, parent=parent)

    return success("评论成功")
