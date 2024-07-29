import uuid

from django.db import models
from django.db.models import Q


# Create your models here.
class User(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class Manager(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class GroupManager(models.Manager):
    def search(self, query):
        lookups = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
        )
        return self.get_queryset().filter(lookups).distinct()


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)
    members = models.ManyToManyField(User, related_name='groups')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GroupManager()


class JoinRequest(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    apply_reason = models.TextField(max_length=200, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, blank=True)


class ProblemGroupManager(models.Manager):
    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query)
        )
        return self.get_queryset().filter(lookups).distinct()


class ProblemGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_problem_groups')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, related_name='problem_groups')
    problem_num = models.IntegerField(default=0)

    objects = ProblemGroupManager()


class ProblemManager(models.Manager):
    def search(self, query, in_fields=True):
        lookups = (
            Q(content__icontains=query)
        )
        if in_fields:
            for field in ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7']:
                lookups |= Q(**{field: query})
        return self.get_queryset().filter(lookups).distinct()

    def search_regex(self, pattern, in_fields=True):
        lookups = (
            Q(content__regex=pattern)
        )
        if in_fields:
            for field in ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7']:
                lookups |= Q(**{field: pattern})
        return self.get_queryset().filter(lookups).distinct()


class Problem(models.Model):
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE, related_name="problems")
    index = models.IntegerField()
    type = models.CharField(max_length=1)  # 'c'(choice)选择题，'b'(blank)填空题
    title = models.CharField(max_length=30)  # 题目，默认情况下需要截取
    content = models.TextField(max_length=1000)  # 题干
    ans_count = models.SmallIntegerField()  # 选择题选项数量，填空题空的个数，小于等于7
    answer = models.CharField(max_length=1, blank=True)  # 仅限选择题
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100, blank=True)
    field3 = models.CharField(max_length=100, blank=True)
    field4 = models.CharField(max_length=100, blank=True)
    field5 = models.CharField(max_length=100, blank=True)
    field6 = models.CharField(max_length=100, blank=True)
    field7 = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    # create_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='problems')

    objects = ProblemManager()


class ProblemPermission(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name="permissions")  # 用户群组
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE, related_name="permissions")  # 问题群组
    permission = models.SmallIntegerField()  # 权限，0 仅可查看，1 可查看并添加问题


# 做题记录
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    result = models.BooleanField(default=False)  # 是否正确
    created_at = models.DateTimeField(auto_now_add=True)


class TemporaryProblemGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problems = models.ManyToManyField(Problem)

class SensitiveWord(models.Model):
    content = models.CharField(max_length=50, unique=True)