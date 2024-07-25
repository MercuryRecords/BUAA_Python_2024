from django.http import JsonResponse

E_USER_NOT_FIND = JsonResponse({"code": 401, "message": "用户不存在"})
E_PROBLEM_GROUP_REPEAT = JsonResponse({"code": 402, "message": "问题组已存在"})
E_PROBLEM_GROUP_NOT_FIND = JsonResponse({"code": 402, "message": "问题组不存在"})
E_PERMISSION_DENIED = JsonResponse({"code": 403, "message": "当前用户没有权限"})
E_PROBLEM_NOT_FIND = JsonResponse({"code": 405, "message": "问题不存在"})
E_TITLE_FORMAT = JsonResponse({"code": 406, "message": "标题非空且长度不能超过50"})
E_DESCRIPTION_FORMAT = JsonResponse({"code": 406, "message": "描述长度不能超过200"})
E_UNKNOWN_TYPE = JsonResponse({"code": 407, "message": "未知题目类型"})
E_PROBLEM_CONTENT_FORMAT = JsonResponse({"code": 407, "message": "题干非空且长度不能超过1000"})
E_PROBLEM_OPTIONS_OR_BLANK_TOO_MUCH = JsonResponse({"code": 407, "message": "选项或填空数量不能超过7"})
E_ILLIGAL_ANSWER = JsonResponse({"code": 407, "message": "答案不合法"})
E_PROBLEM_OPTIONS_OR_BLANK_FORMAT = JsonResponse({"code": 407, "message": "选项或填空内容非空且长度不能超过100"})
E_BAD_POS = JsonResponse({"code": 408, "message": "题目位置不合法"})
E_NO_PROBLEM_GROUP = JsonResponse({"code": 409, "message": "问题组列表为空"})
E_NO_PROBLEM = JsonResponse({"code": 409, "message": "题目列表为空"})
E_PAGE_OVERFLOW = JsonResponse({"code": 410, "message": "页码越界"})
E_GROUP_NOT_FIND = JsonResponse({"code": 411, "message": "用户组不存在"})
E_USER_NOT_IN_GROUP = JsonResponse({"code": 411, "message": "用户不在此用户组中"})
E_PERMISSION_REPEAT = JsonResponse({"code": 412, "message": "分享已存在"})

def success(text):
    return JsonResponse({"code": 200, "message": text})

def success_data(text, data):
    return JsonResponse({"code": 200, "message": text, "data": data})