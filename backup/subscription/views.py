from django.shortcuts import render

# Create your views here.
# subscription/views.py

from django.views import View
from django.http import HttpResponse

class SubscriptionView(View):
    def get(self, request):
        return HttpResponse("Subscription page")

class SubscriptionDetailView(View):
    def get(self, request, id):
        return HttpResponse(f"Subscription detail for ID: {id}")
