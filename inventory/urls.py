from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('location/<int:location_pk>/stock/new/', views.stock_item_create, name='stock_item_create'),
    path('stock/<int:stock_item_pk>/movement/', views.add_movement, name='add_movement'),
]
