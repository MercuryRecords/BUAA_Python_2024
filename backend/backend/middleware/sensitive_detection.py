from django.utils.deprecation import MiddlewareMixin
from database.models import SensitiveWord

import re

# import django.http.request
# request.POST 为该库文件中 QueryDict 类型，其中包含 setlist 方法

# 此处设置要屏蔽敏感词的接口和字段
sensitive_keys = {
    '/api/user_register': ['username'],
    '/api/group_create': ['group_name', 'group_description'],
    '/api/group_apply_to_join': ['apply_reason'],
    '/api/problem_group_create': ['title', 'description', 'tags[]'],
    '/api/problem_group_update': ['title', 'description', 'tags[]'],
    '/api/problem_create': ['title', 'content', 'field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'tags[]'],
    '/api/problem_update': ['title', 'content', 'field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'tags[]'],
    '/api/comment_add': ['content'],
}
sensitive_words = []
compiled_patterns = []
dirty_flag = True

def _censor(text):
    def _replace_sensitive_content(match):
        return '*' * len(match.group(0))
    for pattern in compiled_patterns:
        text = pattern.sub(_replace_sensitive_content, text)
    return text

def setflag():
    global dirty_flag
    dirty_flag = True

class SensitiveDetection(MiddlewareMixin):
    def process_request(self, request):
        request_path = request.path_info
        if request_path.endswith('/'):
            request_path = request_path[:-1]
        
        for path in sensitive_keys.keys():
            if path == request_path:
                keys = sensitive_keys[path]
                # 开始准备敏感词过滤
                global sensitive_words, compiled_patterns, dirty_flag
                if dirty_flag:
                    sensitive_words = SensitiveWord.objects.values_list('content', flat=True)
                    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in sensitive_words]
                    dirty_flag = False
                
                request.POST._mutable = True # 允许修改请求内容

                for key in keys:
                    if key in request.POST:
                        # 为同时兼容字段为单值和列表的情况，使用 getlist / setlist
                        content_list = request.POST.getlist(key)
                        new_content_list = [_censor(s) for s in content_list]
                        request.POST.setlist(key, new_content_list)
                
                request.POST._mutable = False
                break
        
