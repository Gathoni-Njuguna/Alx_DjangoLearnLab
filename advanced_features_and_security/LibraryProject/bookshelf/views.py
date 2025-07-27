from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from .forms import ExampleForm

@login_required
def article_list(request):
    if not request.user.has_perm('articles.can_view'):
        raise PermissionDenied
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

@permission_required('articles.can_create', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/create.html', {'form': form})

@permission_required('articles.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/edit.html', {'form': form, 'article': article})

@permission_required('articles.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/delete.html', {'article': article})

def list_books(request):
    books = Book.objects.all()  # Using Book.objects.all() as requested
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.exceptions import SuspiciousOperation
from .models import Book
from .forms import SearchForm

# Safe search example using Django ORM
@require_http_methods(["GET"])
def book_search(request):
    form = SearchForm(request.GET or None)
    
    if form.is_valid():
        # Safe query using Django ORM (parameterized)
        books = Book.objects.filter(
            title__icontains=form.cleaned_data['query']
        )[:100]  # Limit results
        
        # Never do this: Book.objects.raw(f"SELECT * FROM books WHERE title LIKE '%{request.GET['query']}%'")
    else:
        books = Book.objects.none()
        raise SuspiciousOperation("Invalid search input")
    
    return render(request, 'books/search.html', {'books': books, 'form': form})

# Safe file upload example
def upload_book(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Validate file type and size
            uploaded_file = request.FILES['file']
            if uploaded_file.content_type not in ['application/pdf', 'application/epub+zip']:
                raise SuspiciousOperation("Invalid file type")
            if uploaded_file.size > 10*1024*1024:  # 10MB limit
                raise SuspiciousOperation("File too large")
            
            # Process the file
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookUploadForm()
    
    return render(request, 'books/upload.html', {'form': form})