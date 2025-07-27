from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm

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