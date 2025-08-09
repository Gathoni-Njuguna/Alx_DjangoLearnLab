from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .permissions import IsCreatorOrReadOnly
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Add both filtering and ordering backends
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    
    # Specify ordering fields
    ordering_fields = [
        'title', 
        'id',
        'created_at', 
        'updated_at',
        # Add more fields as needed
    ]
    
    # Default ordering
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the creator to the current user
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """Custom response format for creation"""
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'message': 'Book created successfully',
            'data': response.data
        }, status=status.HTTP_201_CREATED)

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated & IsCreatorOrReadOnly]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        # Update last modified by
        serializer.save(last_modified_by=self.request.user)

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Book deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)