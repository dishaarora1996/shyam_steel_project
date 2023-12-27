from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

from .models import Task, ToDOUsers

class TaskForm(forms.ModelForm):

    task_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
    completed_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%d-%m-%Y'],
        )
    due_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%d-%m-%Y'],
        )

    class Meta:
        model = Task
        fields = ["task_name", "task_note", "assignee", "completed", "completed_at",\
            "due_at", "followers", "project_id", "workspace_id"]


class CustomAuth(AuthenticationForm):

    class Meta:
        model = ToDOUsers
        fields = "__all__"