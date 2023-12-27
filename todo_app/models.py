from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class ToDOUsers(AbstractUser):
    '''User model for ToDo app from Django AbstractUser'''
    gid = models.CharField(max_length=225, blank=True, default="")
    photo_url = models.CharField(max_length=225, blank=True, default="")
    resource_type = models.CharField(max_length=225, blank=True, default="")
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        )
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.')
    )

    def __str__(self):
        return self.username


class Workspace(models.Model):
    workspace_id = models.BigAutoField(primary_key=True)
    ws_gid = models.CharField(max_length=225, blank=True, default="")
    ws_name = models.CharField(max_length=225, blank=True, default="")
    resource_type = models.CharField(max_length=225, blank=True, default="")
    is_organisation = models.BooleanField(default=False)
    email_domain = models.TextField(blank=True, default="")
    todo_user = models.ForeignKey(
        ToDOUsers, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.ws_name

class Project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_gid = models.CharField(max_length=225, blank=True, default="")
    project_name = models.CharField(max_length=225, blank=True, default="")
    resource_type = models.CharField(max_length=225, blank=True, default="")
    archived = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    follower = models.CharField(max_length=225, blank=True, default="")
    member = models.CharField(max_length=225, blank=True, default="")
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(
        ToDOUsers, on_delete=models.CASCADE, blank=True, null=True)
    workspace_id = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_gid = models.CharField(max_length=225, blank=True, default="")
    task_name = models.CharField(max_length=225, blank=True, default="")
    task_note = models.CharField(max_length=225, blank=True, default="")
    resource_type = models.CharField(max_length=225, blank=True, default="")
    resource_subtype = models.CharField(max_length=225, blank=True, default="")
    assignee = models.ForeignKey(
        ToDOUsers,
        on_delete=models.CASCADE,
        related_name="task_assignee",
        blank=True, null=True)
    assignee_status = models.CharField(max_length=225, blank=True, default="")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        ToDOUsers,
        on_delete=models.CASCADE,
        related_name="task_creator",
        blank=True, null=True)
    due_at = models.DateField(blank=True, null=True)
    followers = models.CharField(max_length=225, blank=True, default="")
    project_id = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)
    workspace_id = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.task_name