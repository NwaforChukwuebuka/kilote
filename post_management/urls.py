# post_management/urls.py

from django.urls import path
from .views import CreatePostView, ListPostView, DetailPostView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('list/', ListPostView.as_view(), name='list_posts'),
    path('detail/<int:pk>/', DetailPostView.as_view(), name='detail_post'),
]
