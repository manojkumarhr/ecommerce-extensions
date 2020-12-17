from django.urls import path

from . import views

urlpatterns = [
    path('', views.listener, name='listener'),
    path('transaction_approved/', views.transaction_approved, name='transaction_approved'),
    path('transaction_pending/', views.transaction_pending, name='transaction_pending'),
    path('transaction_declined/', views.transaction_declined, name='transaction_declined'),
]