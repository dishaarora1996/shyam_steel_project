from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .utility import asana_calling, create_asana_task, delete_asana_task, wokspace_detail, project_detail, task_detail
from .models import Project, Workspace, Task, ToDOUsers
from .forms import TaskForm, CustomAuth

from django.contrib.auth.views import LoginView

@csrf_protect
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuth(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list')
    else:
        form = CustomAuth()

    return render(request, 'login.html', {'form': form})

@login_required
def index(request):
    # import pdb;pdb.set_trace()
    data_list = []
    user_data = asana_calling()
    user_info = ToDOUsers.objects.get(id=request.user.id)
    user_info.gid = user_data.get("data").get("gid")
    user_info.photo_url = user_data.get("data").get("photo") if user_data.get("data").get("photo") else ""
    user_info.resource_type = user_data.get("data").get("resource_type")
    user_info.save()
    workspace_ids = user_data.get("data").get("workspaces")
    for workspace in workspace_ids:
        workspace_details = Workspace.objects.filter(ws_gid=workspace.get('gid')).first()
        if not workspace_details:
            temp_workspace = wokspace_detail(workspace.get("gid"))
            temp = {
                "ws_gid": temp_workspace.get("data").get("gid"),
                "ws_name": temp_workspace.get("data").get("name"),
                "resource_type": temp_workspace.get("data").get("resource_type"),
                "is_organisation": temp_workspace.get("data").get("is_organization"),
                "email_domain": temp_workspace.get("data").get("email_domains"),
                "todo_user": user_info
            }
            Workspace.objects.create(**temp)
        projects = asana_calling(workspace_id=workspace.get("gid"))
        for project in projects.get("data"):
            project_details = Project.objects.filter(
                project_gid=project.get("gid")).first()
            if not project_details:
                temp_project = project_detail(project_id=project.get("gid"))
                temp = {
                    "project_gid": temp_project.get("data").get("gid"),
                    "project_name": temp_project.get("data").get("gid"),
                    "resource_type": temp_project.get("data").get("resource_type"),
                    "archived": temp_project.get("data").get("archived"),
                    "completed": temp_project.get("data").get("completed"),
                    "follower": temp_project.get("data").get("followers")[0].get("gid"),
                    "member": temp_project.get("data").get("members")[0].get("gid"),
                    "public": temp_project.get("data").get("public"),
                    "owner" : user_info,
                    "workspace_id" : Workspace.objects.filter(
                        ws_gid=temp_project.get("data").get("workspace").get("gid")).first()
                }
                Project.objects.create(**temp)
            datas = asana_calling(project_id=project.get("gid"))
            for data in datas.get("data"):
                task_info = Task.objects.filter(task_gid=data.get("gid")).first()
                if not task_info:
                    temp_task = task_detail(data.get("gid"))
                    temp = {
                        "task_gid": temp_task.get("data").get("gid"),
                        "task_name": temp_task.get("data").get("name"),
                        "task_note": temp_task.get("data").get("notes"),
                        "resource_type": temp_task.get("data").get("resource_type"),
                        "resource_subtype": temp_task.get("data").get("resource_subtype"),
                        "assignee_status" : temp_task.get("data").get("assignee_status"),
                        "completed" : temp_task.get("data").get("completed"),
                        "completed_at": temp_task.get("data").get("completed_at"),
                        "created_by": user_info,
                        "followers": temp_task.get("data").get("followers")[0].get("gid"),
                        "project_id": Project.objects.filter(
                            project_gid=temp_task.get("data").get("projects")[0].get("gid")).first(),
                        "workspace_id": Workspace.objects.filter(
                            ws_gid=temp_task.get("data").get("workspace").get("gid")).first(),
                        "assignee": user_info
                        }
                    Task.objects.create(**temp)
    task= Task.objects.all()
    context = {"data": task}
    return render(request, 'list.html', context)


def create_task(request):
    task_list = Task.objects.all()

    task_forms = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            create_asana_task(request.POST)
        return redirect('list')
    context = {"task": task_list, "forms": task_forms}
    return render(request, 'create.html', context)

def update_task(request, pk):
    task = Task.objects.get(task_id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        task = Task.objects.filter(task_id=pk).first()
        if form.is_valid():
            if task:
                form.save()
                create_asana_task(request.POST, task_id=task.task_gid, update=True)
            return redirect('list')

    context = {'form': form}
    return render(request, 'update-form.html', context)


def delete_task(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        task = Task.objects.filter(task_id=pk).first()
        if task:
            delete_task = delete_asana_task(task.task_gid)
            if delete_task:
                item.delete()
        return redirect('list')
    context = {'item':item}
    return render(request, 'tasks/delete.html', context)