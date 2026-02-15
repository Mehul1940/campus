from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications, name='list'),
    path('delete/<int:pk>/', views.delete_notification, name='delete'),
    path('announcements/', views.announcements, name='announcements'),
]