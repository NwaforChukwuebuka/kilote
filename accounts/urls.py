from django.urls import path
from .views import SignupView, LoginView, ProfileView, EditProfileView, logout_view

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),  # New URL
    path('logout/', logout_view, name='logout'),
]
