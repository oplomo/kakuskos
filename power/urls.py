from django.urls import path
from . import views

# app_name = "power"

urlpatterns = [
    # Homepage
    path("", views.home, name="home"),
    path('booking-success/', views.booking_success, name='booking_success'),

    # Services
    path("services/", views.all_services, name="all_services"),
    # Case Studies
    path("case-studies/<int:id>/", views.case_study_detail, name="case_study_detail"),
    # ESG Resources
    # path("esg-resources/", views.esg_resources, name="esg_resources"),
    # About page (to be implemented later)
    path("about/", views.about, name="about"),
    # Contact page
    path("contact/", views.contact, name="contact"),
    # Admin dashboard
    
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-conditions/", views.terms_conditions, name="terms_conditions"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    
    
    
    path('adm/dashboard/', views.admin_dashboard, name='adm_dashboard'),
    path('adm/analytics/', views.business_analytics, name='business_analytics'),
    
    # Service management
    path('adm/services/', views.service_list, name='service_list'),
    path('adm/services/edit/<slug:slug>/', views.edit_service, name='edit_service'),
    
    # Case study management
    path('adm/case-studies/', views.case_study_list, name='case_study_list'),
    path('adm/case-studies/add/', views.add_case_study, name='add_case_study'),
    path('adm/case-studies/edit/<int:pk>/', views.edit_case_study, name='edit_case_study'),
    path('adm/case-studies/delete/<int:pk>/', views.delete_case_study, name='delete_case_study'),
    
    # Service request management
    path('adm/service-requests/', views.service_request_list, name='service_request_list'),
    path('adm/service-requests/<int:pk>/complete/', views.mark_request_completed, name='mark_request_completed'),
    
    # Installation projects
    path('adm/projects/', views.project_list, name='project_list'),
    path('adm/projects/add/', views.add_project, name='add_project'),
    path('adm/projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    
    # Monthly metrics
    path('adm/metrics/', views.monthly_metrics, name='monthly_metrics'),
    path('adm/metrics/add/', views.add_monthly_metric, name='add_monthly_metric'),
]



