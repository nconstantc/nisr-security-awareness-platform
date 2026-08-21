from django.urls import path
from . import views

urlpatterns = [
    path('track/<int:campaign_id>/<int:employee_id>/', views.track_phishing_click, name='track-phishing'),
    path('education/', views.phishing_education, name='phishing-education'),
    path('api/risk-employees/', views.get_phishing_risk_employees, name='phishing-risk-employees'),
    path('report/', views.report_phishing, name='phishing-report'),
    path('report-success/', views.report_success, name='phishing-report-success'),
]