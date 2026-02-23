from django.urls import path
from . import views

app_name = 'tax'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('rates/', views.rates, name='rates'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
]
