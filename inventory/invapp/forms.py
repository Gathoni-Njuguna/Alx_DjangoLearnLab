from django import forms
from .models import Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ['name', 'sku', 'category', 'description', 'price', 'stock', 'supplier']
        widgets = {
            'product_id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),   
        }
        labels = {
            'product_id': 'Product ID',
            'name': 'Product Name',
            'sku': 'SKU',
            'category': 'Category',
            'description': 'Description',
            'price': 'Price',
            'stock': 'Stock Quantity',
            'supplier': 'Supplier',
        }