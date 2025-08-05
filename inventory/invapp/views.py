from django.shortcuts import render,redirect
from .forms import ProductForm
from .models import Product

# Create your views here.
def home_view(request):
    return render(request, 'invapp/home.html')
#create views for the inventory app
def product_create_view(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('product_list')
         # Reset the form after saving
    return render(request, 'invapp/productform.html', {'form': form})
# List all products
def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'invapp/productlist.html', {'products': products})
# Update a product
def product_update_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'invapp/productform.html', {'form': form, 'product': product})
# Delete a product
def product_delete_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'invapp/removeproduct.html', {'product': product})