from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.poll_manager, name='home'),
    path('users/', views.user_list, name='users'),
    path('create/', views.create_poll, name='create'),
    path('statistics/', views.poll_statistics, name='statistics'),
    path('content/', views.content_manager, name='content'),
    path('content/<int:content_id>/delete/', views.delete_content, name='delete_content'),
    path('change_user_role/<int:user_id>/<str:new_role>/', views.change_user_role, name='change_user_role'),
    path('manage_user/<int:user_id>/', views.manage_user, name='manage_user'),
    path('toggle_user/<int:user_id>/', views.toggle_user, name='toggle_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('<int:poll_id>/edit/', views.edit_poll, name='edit'),
    path('<int:poll_id>/delete/', views.delete_poll, name='delete'),
    path('export-pdf/<int:poll_id>/', views.export_poll_pdf, name='export_pdf'),
]
