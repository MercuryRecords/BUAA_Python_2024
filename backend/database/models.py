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