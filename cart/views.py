from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from catalog.models import Product
from .models import CartItem
from .utils import get_or_create_cart

@login_required
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, is_active=True)
    cart = get_or_create_cart(request.user)
    qty = int(request.POST.get('quantity', 1) or 1)
    qty = max(1, min(qty, 999))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = qty
    else:
        item.quantity += qty
    item.save()
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('cart:cart_detail')

@login_required
def update_item(request, item_pk):
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, pk=item_pk, cart=cart)
    qty = int(request.POST.get('quantity', item.quantity) or item.quantity)
    qty = max(1, min(qty, 999))
    item.quantity = qty
    item.save()
    messages.success(request, 'Cart updated.')
    return redirect('cart:cart_detail')

@login_required
def remove_item(request, item_pk):
    cart = get_or_create_cart(request.user)
    item = get_object_or_404(CartItem, pk=item_pk, cart=cart)
    item.delete()
    messages.success(request, 'Item removed.')
    return redirect('cart:cart_detail')

@login_required
def cart_count_json(request):
    cart = get_or_create_cart(request.user)
    count = sum([i.quantity for i in cart.items.all()])
    return JsonResponse({'count': count})
