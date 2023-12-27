from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Task, Workspace, Project, ToDOUsers


admin.site.register(Task)
admin.site.register(Workspace)
admin.site.register(Project)
admin.site.register(ToDOUsers, UserAdmin)