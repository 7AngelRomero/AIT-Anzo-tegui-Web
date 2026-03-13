from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.poll_list, name='list'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/answer/', views.answer_poll, name='answer'),
    path('<int:poll_id>/submit/', views.submit_poll, name='submit'),
    path('<int:poll_id>/results/', views.poll_results, name='results'),
]