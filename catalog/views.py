from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Product, Category

def product_list(request):
    products = Product.objects.filter(is_active=True)
    q = request.GET.get('q', '').strip()
    cat = request.GET.get('cat', '').strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(sku__icontains=q))
    if cat:
        products = products.filter(category__slug=cat)
    categories = Category.objects.all().order_by('name')
    return render(request, 'catalog/product_list.html', {
        'products': products.order_by('name'),
        'categories': categories,
        'q': q,
        'cat': cat,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})
