# dashboard/urls.py

from django.urls import path
from .views import DashboardView, SomeOtherView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),  # Adjust as necessary
    path('some-other/', SomeOtherView.as_view(), name='some_other'),  # Additional paths
]
