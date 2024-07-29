from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

from .models import SensitiveWord
from .errors import *
from .views_problem import _cut_to_page

from backend.middleware.sensitive_detection import setflag


def _add_sensitive_words_by_list(words):
    if not words:
        return E_WORD_LIST_EMPTY

    success_cnt = 0
    for word in words:
        if len(word) > 50:
            error_flag = E_WORD_FORMAT
            continue
        try:
            SensitiveWord.objects.create(content=word)
            success_cnt += 1
        except IntegrityError:
            error_flag = E_WORD_REPEAT

    if not success_cnt:
        return error_flag
    return success_cnt


@require_http_methods(["POST"])
def admin_add_sensitive_words_by_list(request):
    words = request.POST.getlist('words[]')
    success_cnt = _add_sensitive_words_by_list(words)
    if isinstance(success_cnt, JsonResponse):
        return success_cnt

    setflag()
    return success_data("已添加" + str(success_cnt) + "个敏感词", success_cnt)


@require_http_methods(["POST"])
def admin_add_sensitive_words_by_txt_file(request):
    txt_file = request.FILES['file']
    try:
        words = [line.decode(encoding='UTF-8').rstrip('\r\n') for line in txt_file.readlines()]
    except UnicodeDecodeError:
        return E_DECODE_FAILED

    success_cnt = _add_sensitive_words_by_list(words)
    if isinstance(success_cnt, JsonResponse):
        return success_cnt

    setflag()
    return success_data("已添加" + str(success_cnt) + "个敏感词", success_cnt)


@require_http_methods(["POST"])
def admin_delete_sensitive_word(request):
    word = request.POST.get('word')
    check = SensitiveWord.objects.filter(content=word)
    if not check:
        return E_WORD_NOT_FIND
    check.delete()

    setflag()
    return success("成功删除敏感词")


@require_http_methods(["POST"])
def admin_clear_sensitive_word(request):
    SensitiveWord.objects.all().delete()
    setflag()
    return success("已清除所有敏感词")


@require_http_methods(["POST"])
def admin_get_sensitive_word_num(request):
    return success_data("敏感词数量", SensitiveWord.objects.count())


@require_http_methods(["POST"])
def admin_get_sensitive_word_list(request):
    words = SensitiveWord.objects.all()
    to_search = request.POST.get('to_search')
    if to_search:
        words = words.filter(content__icontains=to_search)

    words = _cut_to_page(request, words)
    if isinstance(words, JsonResponse):
        return words

    return success_data("敏感词列表", [word.content for word in words])
