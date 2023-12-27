from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path("list/", views.index, name="list"),
    path("create-task/", views.create_task, name="create_task"),
    path('update-task/<int:pk>/', views.update_task, name="update_task"),
    path('delete/<str:pk>/', views.delete_task, name="delete"),
]
