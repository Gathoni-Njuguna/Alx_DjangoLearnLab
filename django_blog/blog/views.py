from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm

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