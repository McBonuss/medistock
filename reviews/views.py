from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product
from .forms import ReviewForm
from .models import Review

@login_required
def add_review(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, is_active=True)
    try:
        review = Review.objects.get(product=product, user=request.user)
        return redirect('reviews:edit_review', review_pk=review.pk)
    except Review.DoesNotExist:
        review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review posted.')
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {'form': form, 'product': product, 'mode': 'Add'})

@login_required
def edit_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    product = review.product
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated.')
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/review_form.html', {'form': form, 'product': product, 'mode': 'Edit'})

@login_required
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    product_pk = review.product.pk
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('catalog:product_detail', pk=product_pk)
    return render(request, 'reviews/review_delete.html', {'review': review})
