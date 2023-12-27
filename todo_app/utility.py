import requests
import json
from datetime import datetime
from django.conf import settings

from todo_app.models import ToDOUsers

asana_baseurl = settings.ASANA_BASEURL
headers = {
        'Authorization': f"Bearer {settings.ASANA_API_KEY}",
        "accept": "application/json"
        }

def wokspace_detail(workshop_id):
    endpoint = f"/workspaces/{workshop_id}"
    response = requests.get(asana_baseurl+endpoint, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return response

def project_detail(project_id):
    endpoint = f"/projects/{project_id}"
    response = requests.get(asana_baseurl+endpoint, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return response

def task_detail(task_id):
    endpoint = f"/tasks/{task_id}"
    response = requests.get(asana_baseurl+endpoint, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return response

def asana_calling(workspace_id=None, project_id=None):
    if workspace_id is not None and workspace_id != "":
        endpoint = f"/projects?workspace={workspace_id}"
    elif project_id is not None and project_id != "":
        endpoint = f"/tasks?project={project_id}"
    else:
        endpoint = "/users/me"

    
    response = requests.get(asana_baseurl+endpoint, headers=headers)
    if response.status_code == 200:
        response = response.json()
        return response

def create_asana_task(data, task_id=None, update=False):
    creator = ToDOUsers.objects.filter(id=data.get("assignee")).first()
    task_data = {
            "data": {
                "name": data.get("task_name"),
                "resource_subtype": "default_task",
                "approval_status": "pending",
                "assignee_status": "upcoming",
                "completed": False,
                "due_at": data.get("due_at"),
                "liked": True,
                "notes": data.get("task_notes"),
                "start_at": datetime.now(),
                "assignee": creator.gid,
                "followers": [
                    creator.gid
                ],
                "projects": [
                    str(creator.project_set().first().project_gid)
                ],
                "workspace": str(creator.workspace_set.first().ws_gid)
            }
        }
    if update:
        endpoint = f"/tasks/{task_id}"
    else:
        endpoint = "/tasks"
    response = requests.post(asana_baseurl+endpoint, headers=headers, data=json.dumps(task_data))
    if response.status_code == 200:
        response = response.json()
        return response


def delete_asana_task(task_id):
    endpoint = f"/tasks/{task_id}"
    response = requests.delete(asana_baseurl+endpoint, headers=headers)
    if response.status_code == 200:
        return True
