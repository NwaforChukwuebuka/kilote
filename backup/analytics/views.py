from django.shortcuts import render

# Create your views here.
# analytics/views.py

from django.views import View
from django.http import HttpResponse

class AnalyticsView(View):
    def get(self, request):
        return HttpResponse("Analytics overview")

class ReportsView(View):
    def get(self, request):
        return HttpResponse("Reports page")
