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
        path('all_categories/', views.all_categories, name='all_categories'),
        path('all_categories/<int:pk>/edit_category/', views.edit_category, name='edit_category'),
        path('all_categories/<int:pk>/delete_category/', views.delete_category, name='delete_category'),

        path('create_transaction/', views.create_transaction, name='create_transaction'),
        path('all_transactions/', views.all_transactions, name='all_transactions'),
        path('all_transactions/<int:pk>/edit_transaction/', views.edit_transaction, name='edit_transaction'),
        path('all_transactions/<int:pk>/delete_transaction/', views.delete_transaction, name='delete_transaction'),

        path('report_generator/', views.report_generator, name='report_generator'),
        path('report_generator/group_category/', views.group_category, name='group_category'),
]
