from rest_framework import serializers
from .models import Author, Book
from datetime import datetime
class BookSerializer(serializers.ModelSerializer):


    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']
        
    def validate_publication_year(self, value):
        """Ensure publication year is not in the future"""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value
class AuthorSerializer(serializers.ModelSerializer):
    
    books = BookSerializer(
        many=True, 
        read_only=True,  # Prevents creation of books through author serializer
        source='books'   # Uses the related_name from Book model
    )  
    class Meta:
        model = Author
        fields = ['id', 'name']
