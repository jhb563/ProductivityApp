from django.contrib import admin
from todolist.models import User, Project, Task

admin.site.register(Project)
admin.site.register(Task)
