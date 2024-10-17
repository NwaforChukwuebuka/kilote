from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from .models import Post  # Make sure you have a Post model defined
from .forms import PostForm  # Assuming you have a PostForm defined for post creation
from django.contrib.auth.mixins import LoginRequiredMixin  # Import the mixin


# Create your views here.
class CreatePostView(LoginRequiredMixin, View):  # Add the mixin to the view
    login_url = '/accounts/login/'  # Redirect to login page if not logged in
    redirect_field_name = 'next'  # Redirect back to the form after login

    def get(self, request):
        form = PostForm()
        return render(request, 'create_new_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Set the user to the currently logged-in user
            post.save()  # Save the post
            return redirect('dashboard')
        return render(request, 'create_new_post.html', {'form': form})


class ListPostView(View):
    def get(self, request):
        posts = Post.objects.all()  # Retrieve all posts
        return render(request, 'list_posts.html', {'posts': posts})

class DetailPostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  # Get the post or return a 404
        return render(request, 'detail_post.html', {'post': post})

