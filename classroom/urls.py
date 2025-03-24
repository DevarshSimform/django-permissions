from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='classroom/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create/', views.notice_create, name='notice_create'),
    path('list/', views.notice_list, name='notice_list'),
    path('update/<int:pk>/', views.notice_update, name='notice_update'),
    path('delete/<int:pk>/', views.notice_delete, name='notice_delete'),
    path('group/', views.groups, name='groups'),
    path('assign/', views.assign_notice, name='assign_notice'),
    

    # path('test/', views.file_response, name='test'),
]
