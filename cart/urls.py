from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_pk>/', views.add_to_cart, name='add_to_cart'),
    path('item/<int:item_pk>/update/', views.update_item, name='update_item'),
    path('item/<int:item_pk>/remove/', views.remove_item, name='remove_item'),
    path('count.json', views.cart_count_json, name='cart_count_json'),
]
