from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_dashboard, name='customer_dashboard'),
    path('engineer/', views.engineer_dashboard, name='engineer_dashboard')
]
