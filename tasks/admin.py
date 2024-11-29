from django.contrib import admin
from .models import Comment, Task, Status, Assignee, Priorities
# Register your models here.


admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Assignee)
admin.site.register(Priorities)
admin.site.register(Comment)

