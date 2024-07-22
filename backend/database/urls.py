from django.urls import path
from . import views, views_problem, views_ocr

urlpatterns = [
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
    path('group_create', views.group_create, name='group_create'),
    path('group_apply_to_join', views.group_apply_to_join, name='group_apply_to_join'),
    path('group_handle_join_request', views.group_handle_join_request, name='group_handle_join_request'),
    path('group_delete_member', views.group_delete_member, name='group_delete_member'),
    path('group_quit', views.group_quit, name='group_quit'),
    path('group_get_groups', views.group_get_groups, name='group_get_groups'),
    path('group_delete_all', views.group_delete_all, name='group_delete_all'),
    path('group_search', views.group_search, name='group_search'),

    path('problem_group_create', views_problem.problem_group_create),
    path('problem_group_update', views_problem.problem_group_update),
    path('problem_group_delete', views_problem.problem_group_delete),
    path('problem_create', views_problem.problem_create),
    path('problem_update', views_problem.problem_update),
    path('problem_delete', views_problem.problem_delete),
    path('problem_adjust_order', views_problem.problem_adjust_order),
    

    path('pdf/text', views_ocr.pdf_text),
]
