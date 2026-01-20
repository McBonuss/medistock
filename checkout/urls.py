from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.start_checkout, name='start_checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
