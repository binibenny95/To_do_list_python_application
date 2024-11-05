from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    #home page
    path('home_menu', views.home_menu, name='home_menu'),
    path('tasks/create', views.task_create, name='task_create'),
    path('tasks/delete/<int:pk>', views.delete_task, name='delete_task'),
    path('tasks/edit/<int:pk>', views.edit_task, name='edit_task'),
    path('tasks/view/<int:pk>', views.view_task, name='view_task'),
    #download task as pdf
    path('tasks/download/<int:pk>', views.generate_pdf, name='generate_pdf'),

    #Assignee
     path('tasks/create_assignee', views.create_assignee, name='create_assignee'),
     path('tasks/assignee_delete/<int:pk>', views.delete_assignee, name='delete_assignee'),
     path('tasks/edit_assignee/<int:pk>', views.edit_assignee, name='edit_assignee'),

    #Delete ToDo
    path('tasks/delete_todo/<int:pk>', views.delete_todo, name='delete_todo'),

    #Search tasks
    path('tasks/search', views.search_tasks, name='search_tasks'),



]