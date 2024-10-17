from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('', views.statuses_list, name='statuses_list'),
    path('create/', views.status_create, name='status_create'),
]
