from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace with your home view name
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True

def custom_logout(request):
    logout(request)
    return render(request, 'blog/logout.html')

@login_required
def profile(request):
    user = request.user
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None)
    user_form = CustomUserChangeForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if 'update_profile' in request.POST and profile_form.is_valid():
            # Save profile data to session (or extend User model in real implementation)
            request.session['bio'] = profile_form.cleaned_data['bio']
            if profile_form.cleaned_data['profile_picture']:
                request.session['profile_picture'] = profile_form.cleaned_data['profile_picture'].name
            return redirect('profile')
        
        if 'update_user' in request.POST and user_form.is_valid():
            user_form.save()
            return redirect('profile')

    # Get profile data from session
    profile_data = {
        'bio': request.session.get('bio', ''),
        'profile_picture': request.session.get('profile_picture', '')
    }
    
    return render(request, 'blog/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_data': profile_data
    })