from django.contrib import admin
from django.urls import path, include
from api.views import BookList
from rest_framework.routers import DefaultRouter
from api.views import BookViewSet
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
    path('', include(router.urls)),  # This includes all routes registered with the router
]
