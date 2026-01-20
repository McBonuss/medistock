import os
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from cart.utils import get_or_create_cart
from .models import Order, OrderLineItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def _finalize_order(order, user):
    cart = get_or_create_cart(user)
    for item in cart.items.select_related('product'):
        OrderLineItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            line_total_gbp=item.line_total_gbp,
        )
    order.status = Order.STATUS_PAID
    order.save()

    profile = user.profile
    profile.paid_access = True
    profile.save()

    cart.items.all().delete()

@login_required
def start_checkout(request):
    cart = get_or_create_cart(request.user)
    if cart.items.count() == 0:
        messages.info(request, 'Your cart is empty.')
        return redirect('catalog:product_list')

    # Must have at least one location to deliver to
    profile = request.user.profile
    org = profile.organisation
    locations = org.locations.all() if org else []
    if not org or len(locations) == 0:
        messages.error(request, 'Please create an organisation and at least one location before checking out.')
        return redirect('accounts:profile')

    if request.method == 'POST':
        location_id = request.POST.get('location')
        try:
            location = locations.get(id=location_id)
        except Exception:
            messages.error(request, 'Select a valid delivery location.')
            return redirect('checkout:start_checkout')

        order = Order.objects.create(user=request.user, location=location, total_gbp=cart.total_gbp)

        if settings.MOCK_STRIPE_SUCCESS:
            _finalize_order(order, request.user)
            messages.success(request, 'Payment simulated for demo. Inventory dashboard unlocked!')
            return render(request, 'checkout/success.html', {'order': order})

        line_items = []
        for item in cart.items.select_related('product'):
            line_items.append({
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': item.product.name,
                        'description': item.product.sku,
                    },
                    'unit_amount': int(item.product.price_gbp * 100),
                },
                'quantity': item.quantity,
            })

        success_url = request.build_absolute_uri(reverse('checkout:success')) + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = request.build_absolute_uri(reverse('checkout:cancel'))

        checkout_session = stripe.checkout.Session.create(
            mode='payment',
            line_items=line_items,
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(order.id),
            metadata={'order_id': str(order.id)},
        )

        order.stripe_session_id = checkout_session.id
        order.save()

        return redirect(checkout_session.url)

    return render(request, 'checkout/start_checkout.html', {'cart': cart, 'locations': locations})

@login_required
def success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, 'Missing Stripe session.')
        return redirect('catalog:product_list')

    # Verify session and mark order paid
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        messages.error(request, 'Could not verify payment session.')
        return redirect('catalog:product_list')

    order_id = session.metadata.get('order_id') if session.metadata else None
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if session.payment_status == 'paid' and order.status != Order.STATUS_PAID:
        _finalize_order(order, request.user)

        messages.success(request, 'Payment successful. Inventory dashboard unlocked!')

    return render(request, 'checkout/success.html', {'order': order})

@login_required
def cancel(request):
    messages.info(request, 'Payment cancelled. You can try again anytime.')
    return render(request, 'checkout/cancel.html')
