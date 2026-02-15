from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.list_events, name='list'),
    path('<int:event_id>/', views.event_detail, name='detail'),
    path('api/<int:event_id>/register/', views.register_event, name='register'),
    path('api/<int:event_id>/unregister/', views.unregister_event, name='unregister'),
]