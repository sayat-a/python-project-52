from django.urls import path
from task_manager.tags import views


urlpatterns = [
    path('', views.tags_list, name='tags_list'),
    path('create/', views.tag_create, name='tag_create'),
    path('<int:pk>/update/', views.tag_update, name='tag_update'),
    path('<int:pk>/delete/', views.tag_delete, name='tag_delete'),
]
