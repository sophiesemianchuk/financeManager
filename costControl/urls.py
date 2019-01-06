from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
        path('', views.index, name='index'),
        path('login/', auth_views.LoginView.as_view(template_name='log_in.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='log_out.html', next_page='login'), name='logout'),
        path('register/', views.register, name='register'),
        path('profile/', views.home, name='home'),
        path('create_category/', views.create_category, name='create_category'),
]
