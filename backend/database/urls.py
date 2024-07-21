from django.urls import path
from . import views

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

    path('pdf/text', views.pdf_text),
]
