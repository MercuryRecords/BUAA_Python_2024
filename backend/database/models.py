import uuid

from django.db import models
from django.db.models import Q


# Create your models here.
class User(models.Model):
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


class ProblemGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    problem_num = models.IntegerField(default=0)


class Problem(models.Model):
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE)
    index = models.IntegerField()
    type = models.CharField(max_length=1) # 'c'(choice)选择题，'b'(blank)填空题
    content = models.TextField(max_length=1000) # 题干
    ans_count = models.SmallIntegerField() # 选择题选项数量，填空题空的个数，小于等于7
    answer = models.CharField(max_length=1, blank=True) # 仅限选择题
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100, blank=True)
    field3 = models.CharField(max_length=100, blank=True)
    field4 = models.CharField(max_length=100, blank=True)
    field5 = models.CharField(max_length=100, blank=True)
    field6 = models.CharField(max_length=100, blank=True)
    field7 = models.CharField(max_length=100, blank=True)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ProblemPremission(models.Model):
    group = models.ForeignKey(Group, blank=True, on_delete=models.CASCADE) # 用户群组
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE) # 问题群组
    permission = models.SmallIntegerField() # 权限，0 仅可查看，1 可查看并添加问题，2 全部权限
