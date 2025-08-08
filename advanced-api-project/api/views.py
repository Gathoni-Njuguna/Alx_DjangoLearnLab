from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions
from django.http import HttpResponse
from .permissions import IsCreatorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[permissions.AllowAny]
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[permissions.AllowAny]
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[permissions.IsAuthenticated]
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated & IsCreatorOrReadOnly]
    def perform_update(self, serializer):
        serializer.save(last_modified_by=self.request.user)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[permissions.IsAuthenticated & permissions.IsAdminUser]
class BookCreateView(generics.CreateAPIView):
    # ... existing code ...
    
    def create(self, request, *args, **kwargs):
        """Custom response format for creation"""
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Book created successfully',
            'data': response.data
        }, status=status.HTTP_201_CREATED)