from django.urls import path
from . import views
from .api_views import MyBadgesView

urlpatterns = [
    path("my-badges/", MyBadgesView.as_view(), name="my-badges"),
    path('download/<int:badge_id>/', views.download_badge_certificate, name='download-badge'),
]