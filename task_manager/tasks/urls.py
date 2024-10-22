from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
]
