from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .models import Library
# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Using Book.objects.all() as requested
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'].books = context['library'].books.all()  # Also using .all() here
        return context