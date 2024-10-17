from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('create/', views.SignUpView.as_view(), name='signup'),
    path('<int:pk>/update/', views.user_update, name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
]
