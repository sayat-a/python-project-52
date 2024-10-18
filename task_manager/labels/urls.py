from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.labels_list, name='labels_list'),
    path('create/', views.label_create, name='label_create'),
    path('<int:pk>/update/', views.label_update, name='label_update'),
    path('<int:pk>/delete/', views.label_delete, name='label_delete'),
]
