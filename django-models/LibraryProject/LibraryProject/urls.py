from django.contrib import admin
from django.urls import path, include
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
        # Authentication URLs using class-based views
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]