from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('manager/', views.poll_manager, name='poll_manager'),
    path('create/', views.create_poll, name='create_poll'),
    path('user/<int:user_id>/role/<str:new_role>/', views.change_user_role, name='change_user_role'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/submit/', views.submit_poll, name='submit_poll'),
    path('<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
]