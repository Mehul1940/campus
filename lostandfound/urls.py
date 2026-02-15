from django.urls import path
from . import views

app_name = 'lostandfound'

urlpatterns = [
    path('', views.list_items, name='list'),
    path('report/', views.report_item, name='report'),
    path('claim/<int:item_id>/', views.claim_item, name='claim'),
    path('return/<int:item_id>/', views.return_item, name='return'),
]