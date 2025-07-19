from django.contrib import admin
from django.urls import path, include
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
        # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]