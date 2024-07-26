from django.urls import path
from . import views, views_problem, views_ocr, views_admin

urlpatterns = [
    path('user_register', views.user_register, name='user_register'),
    path('user_login', views.user_login, name='user_login'),
    path('group_create', views.group_create, name='group_create'),
    path('group_apply_to_join', views.group_apply_to_join, name='group_apply_to_join'),
    path('group_handle_join_request', views.group_handle_join_request, name='group_handle_join_request'),
    path('group_delete_member', views.group_delete_member, name='group_delete_member'),
    path('group_quit', views.group_quit, name='group_quit'),
    path('group_get_groups', views.group_get_groups, name='group_get_groups'),
    path('group_get_groups_created', views.group_get_groups_created, name='group_get_groups_created'),
    path('group_get_groups_joined', views.group_get_groups_joined, name='group_get_groups_joined'),
    path('group_get_members', views.group_get_members, name='group_get_members'),
    path('group_delete_all', views.group_delete_all, name='group_delete_all'),
    path('group_search', views.group_search, name='group_search'),

    # 初版接口
    path('group_join_forced', views.group_join_forced, name='group_join_forced'),

    path('admin_register_user', views_admin.admin_register_user, name='admin_register_user'),
    path('admin_delete_user', views_admin.admin_delete_user, name='admin_delete_user'),
    path('admin_get_user_list', views_admin.admin_get_user_list, name='admin_get_user_list'),
    path('admin_get_group_list', views_admin.admin_get_group_list, name='admin_get_group_list'),
    path('admin_delete_group', views_admin.admin_delete_group, name='admin_delete_group'),
    path('admin_add_user_to_group', views_admin.admin_add_user_to_group, name='admin_add_user_to_group'),
    path('admin_remove_user_from_group', views_admin.admin_remove_user_from_group, name='admin_delete_user_from_group'),
    path("admin_edit_group_info", views_admin.admin_edit_group_info, name="admin_edit_group_info"),

    path('ocr', views_ocr.ocr_view),

    path('problem_group_create', views_problem.problem_group_create),
    path('problem_group_update', views_problem.problem_group_update),
    path('problem_group_delete', views_problem.problem_group_delete),
    path('problem_share', views_problem.problem_share),
    path('problem_create', views_problem.problem_create),
    path('problem_update', views_problem.problem_update),
    path('problem_delete', views_problem.problem_delete),
    path('problem_adjust_order', views_problem.problem_adjust_order),
    
    path('get_problems', views_problem.get_problems_with_permissions),
    path('get_problems_num', views_problem.get_problem_num_with_permissions),
]
