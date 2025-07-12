from django.contrib import admin
from .models import Book
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')  
    # Add search functionality
    search_fields = ('title', 'author')  
    # Add filters by publication year
    list_filter = ('publication_year',)  

# Register with customizations
admin.site.register(Book, BookAdmin)