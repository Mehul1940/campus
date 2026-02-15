from django.urls import path
from . import views

app_name = 'cleanliness'

urlpatterns = [
    path('', views.list_reports, name='list'),
    path('submit/', views.submit_report, name='submit'),
]