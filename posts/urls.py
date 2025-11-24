from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('manager/', views.poll_manager, name='poll_manager'),
    path('users/', views.user_list, name='user_list'),
    path('create/', views.create_poll, name='create_poll'),
    path('change_user_role/<int:user_id>/<str:new_role>/', views.change_user_role, name='change_user_role'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/answer/', views.answer_poll, name='answer_poll'),
    path('<int:poll_id>/submit/', views.submit_poll, name='submit_poll'),
    path('<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
    path('content/', views.content_manager, name='content_manager'),
    path('content/<int:content_id>/delete/', views.delete_content, name='delete_content'),
    path('statistics/', views.poll_statistics, name='poll_statistics'),
]