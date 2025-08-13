from django.urls import path
from . import views
from .views import CustomLoginView, custom_logout

urlpatterns = [
    # ... existing blog URLs ...
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]