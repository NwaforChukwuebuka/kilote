# subscription/urls.py

from django.urls import path
from .views import SubscriptionView, SubscriptionDetailView

urlpatterns = [
    path('', SubscriptionView.as_view(), name='subscription'),
    path('<int:id>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
]
