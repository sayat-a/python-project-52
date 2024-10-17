from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('', views.statuses_list, name='statuses_list'),
    path('create/', views.status_create, name='status_create'),
    path('<int:pk>/update/', views.status_update, name='status_update'),
    path('<int:pk>/delete/', views.status_delete, name='status_delete'),
]
