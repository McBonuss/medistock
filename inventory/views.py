from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Location
from .decorators import paid_access_required
from .forms import StockItemForm, StockMovementForm
from .models import StockItem, StockMovement

@login_required
@paid_access_required
def dashboard(request):
    profile = request.user.profile
    org = profile.organisation
    if not org:
        messages.error(request, 'Please create or join an organisation first.')
        return redirect('accounts:profile')

    locations = org.locations.all()
    location_id = request.GET.get('location')
    location = locations.first()
    if location_id:
        try:
            location = locations.get(id=location_id)
        except Exception:
            pass

    stock_items = StockItem.objects.filter(location=location).select_related('product').order_by('product__name') if location else []

    return render(request, 'inventory/dashboard.html', {
        'locations': locations,
        'selected_location': location,
        'stock_items': stock_items,
    })

@login_required
@paid_access_required
def stock_item_create(request, location_pk):
    profile = request.user.profile
    if profile.role != profile.ROLE_ORG_ADMIN:
        messages.error(request, 'Only organisation admins can add stock items.')
        return redirect('inventory:dashboard')

    location = get_object_or_404(Location, pk=location_pk, organisation=profile.organisation)

    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            stock_item = form.save(commit=False)
            stock_item.location = location
            try:
                stock_item.save()
            except Exception:
                messages.error(request, 'That product is already tracked for this location.')
                return redirect('inventory:dashboard')
            messages.success(request, 'Stock item created.')
            return redirect('inventory:dashboard')
    else:
        form = StockItemForm()

    return render(request, 'inventory/stock_item_form.html', {'form': form, 'location': location})

@login_required
@paid_access_required
def add_movement(request, stock_item_pk):
    profile = request.user.profile
    stock_item = get_object_or_404(StockItem, pk=stock_item_pk, location__organisation=profile.organisation)

    if request.method == 'POST':
        form = StockMovementForm(request.POST, stock_item=stock_item)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.stock_item = stock_item
            movement.created_by = request.user
            movement.save()

            # Apply movement to stock
            if movement.movement_type == StockMovement.TYPE_IN:
                stock_item.qty_on_hand += movement.quantity
            elif movement.movement_type == StockMovement.TYPE_OUT:
                stock_item.qty_on_hand = max(0, stock_item.qty_on_hand - movement.quantity)
            else:
                # Adjustment: treat as absolute set if reason contains 'set:' else add
                stock_item.qty_on_hand = stock_item.qty_on_hand  # no automatic change
            stock_item.save()

            messages.success(request, 'Stock updated.')
            return redirect(f"{request.build_absolute_uri('/inventory/')}?location={stock_item.location.id}")
    else:
        form = StockMovementForm(stock_item=stock_item)

    return render(request, 'inventory/movement_form.html', {'form': form, 'stock_item': stock_item})
