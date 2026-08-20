from django.urls import path
from . import views

urlpatterns = [
    path('track/<int:campaign_id>/<int:employee_id>/', views.track_phishing_click, name='track-phishing'),
    path('education/', views.phishing_education, name='phishing-education'),
]