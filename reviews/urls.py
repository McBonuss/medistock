from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_pk>/add/', views.add_review, name='add_review'),
    path('<int:review_pk>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_pk>/delete/', views.delete_review, name='delete_review'),
]
