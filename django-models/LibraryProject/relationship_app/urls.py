from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from .views import admin_view, librarian_view, member_view
urlpatterns = [
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    # Authentication URLs using class-based views
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    # Role-based URLs
    path('admin/', admin_view, name='admin-view'),
    path('librarian/', librarian_view, name='librarian-view'),
    path('member/', member_view, name='member-view'),
    
]