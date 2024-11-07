from datetime import timezone

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Assignee(models.Model):
    name = models.TextField(verbose_name="Assignee Name", max_length=100)
    email = models.EmailField(verbose_name="Assignee Email", max_length=100, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.TextField(verbose_name="Task Status", max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Priorities(models.Model):
    name = models.TextField(verbose_name="Task Priority", max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Todo(models.Model):
    name = models.TextField(verbose_name="Todo task", max_length=100)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name


class Task(models.Model):
    description = models.TextField(verbose_name="Description", max_length=1000)
    hours = models.IntegerField(verbose_name="Hours", default=0)
    date = models.DateTimeField(verbose_name="Date", auto_now=True)
    assigned_to = models.ForeignKey(Assignee, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    priority = models.ForeignKey(Priorities, on_delete=models.CASCADE, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
