from django.urls import path
from . import views

app_name = 'tax'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('rates/', views.tax_rates_list, name='rates'),
    path('reports/', views.dashboard, name='reports'),


    # TaxRate
    path('tax_rates/', views.tax_rates_list, name='tax_rates_list'),
    path('tax_rates/add/', views.tax_rate_add, name='tax_rate_add'),
    path('tax_rates/<uuid:pk>/edit/', views.tax_rate_edit, name='tax_rate_edit'),
    path('tax_rates/<uuid:pk>/delete/', views.tax_rate_delete, name='tax_rate_delete'),
    path('tax_rates/<uuid:pk>/toggle/', views.tax_rate_toggle_status, name='tax_rate_toggle_status'),
    path('tax_rates/bulk/', views.tax_rates_bulk_action, name='tax_rates_bulk_action'),

    # TaxReport
    path('tax_reports/', views.tax_reports_list, name='tax_reports_list'),
    path('tax_reports/add/', views.tax_report_add, name='tax_report_add'),
    path('tax_reports/<uuid:pk>/edit/', views.tax_report_edit, name='tax_report_edit'),
    path('tax_reports/<uuid:pk>/delete/', views.tax_report_delete, name='tax_report_delete'),
    path('tax_reports/bulk/', views.tax_reports_bulk_action, name='tax_reports_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
