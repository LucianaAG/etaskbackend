from django.db import models
from user.models import User
from django.contrib.postgres.fields import ArrayField
from notifications.models import Publisher

class SubTaskItem(models.Model):

    item = models.CharField(max_length=100)
    done = models.BooleanField(default=False)


class SubTask(models.Model):

    name = models.CharField(max_length=100)
    item = models.ManyToManyField(SubTaskItem, blank=True)


class Task(models.Model, Publisher):

    subscribers = ArrayField(models.IntegerField(), blank=True, default=list)
    task_name = models.CharField(max_length=100)
    task_date = models.DateField()
    task_description = models.TextField(max_length=300)
    task_category = models.CharField(max_length=100)
    task_users_id = ArrayField(models.IntegerField(), blank=True)
    task_priority = models.CharField(max_length=100)
    task_status = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100, primary_key=True)
    sub_tasks = models.ManyToManyField(SubTask, blank=True, null=True)

    def attach(self, subscriber_id):
        self.subscribers.append(subscriber_id)

    def dettach(self, subscriber_id):
        self.subscribers.remove(subscriber_id)
        
    def notify(self, state):
        for subscriber_id in self.subscribers:
            user = User.objects.get(pk=subscriber_id)
            user.update(self.task_id, state)
