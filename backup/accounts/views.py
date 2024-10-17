from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout
from django.views.generic import TemplateView
from .forms import UserUpdateForm  # creates a form for user update

# Signup view
class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic validation for password confirmation
        if password != confirm_password:
            form_error = "Passwords do not match."
            return render(request, self.template_name, {'form_error': form_error})

        # Create user using the User model
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name  # Ensure this is set
        )
        user.save()
        login(request, user)  # Log the user in after signing up
        return redirect('profile')  # Redirect to profile or any desired page


from django.contrib import messages  # Import messages module for feedback

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try to get the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # Authenticate with the username and password
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')  # Success message
                return redirect('profile')  # Redirect to profile after login
            else:
                messages.error(request, 'Invalid password.')  # Invalid password message
        else:
            messages.error(request, 'Invalid email.')  # Invalid email message

        # If authentication fails, recreate the form to pass it back to the template
        form = AuthenticationForm(data=request.POST)
        return render(request, self.template_name, {'form': form})

# Profile view (requires login)
@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Pass the logged-in user to the template
        return context



@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    template_name = 'edit_profile.html'

    def get(self, request):
        user = request.user
        form = UserUpdateForm(instance=user)  # Use the form with existing user data
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user details
            return redirect('profile')  # Redirect to profile after saving
        return render(request, self.template_name, {'form': form})


# Logout view (simple redirect after logging out)
def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to login after logout
