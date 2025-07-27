from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from .models import Book
import datetime

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')

class ExampleForm(forms.Form):
    """
    Example form demonstrating security best practices including:
    - Field validation
    - Input sanitization
    - CSRF protection (automatically included)
    - Secure file upload handling
    """
    
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the book title"
    )
    
    author = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter the author's name"
    )
    
    publication_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Select publication date"
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        help_text="Optional book description"
    )
    
    cover_image = forms.ImageField(
        required=False,
        help_text="Upload cover image (max 2MB)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    def clean_title(self):
        title = self.cleaned_data['title']
        # Basic sanitization
        title = title.strip()
        if not title:
            raise ValidationError("Title cannot be empty")
        return title
    
    def clean_publication_date(self):
        date = self.cleaned_data['publication_date']
        if date > datetime.date.today():
            raise ValidationError("Publication date cannot be in the future")
        return date
    
    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')
        if image:
            if image.size > 2 * 1024 * 1024:  # 2MB limit
                raise ValidationError("Image file too large (max 2MB)")
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError("Only JPEG or PNG images allowed")
        return image
    
    def clean(self):
        cleaned_data = super().clean()
        # Example of cross-field validation
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        
        if title and author and title.lower() == author.lower():
            raise ValidationError("Title and author cannot be identical")
        
        return cleaned_data

# ModelForm example for Book model
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'description', 'cover_image']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'