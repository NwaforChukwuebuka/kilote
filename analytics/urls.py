# analytics/urls.py

from django.urls import path
from .views import AnalyticsView, ReportsView

urlpatterns = [
    path('', AnalyticsView.as_view(), name='analytics'),
    path('reports/', ReportsView.as_view(), name='reports'),
]
