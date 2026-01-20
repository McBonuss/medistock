from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, LocationForm, OrganisationSetupForm
from .models import Location

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('catalog:product_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    profile = request.user.profile
    form = OrganisationSetupForm() if not profile.organisation else None
    if request.method == 'POST' and not profile.organisation:
        form = OrganisationSetupForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, 'Organisation linked. You can now manage locations and checkout.')
            return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'org_form': form})

@login_required
def location_list(request):
    profile = request.user.profile
    if profile.role != profile.ROLE_ORG_ADMIN:
        messages.error(request, 'Only organisation admins can manage locations.')
        return redirect('accounts:profile')
    org = profile.organisation
    locations = org.locations.all() if org else []
    return render(request, 'accounts/location_list.html', {'locations': locations})

@login_required
def location_create(request):
    profile = request.user.profile
    if profile.role != profile.ROLE_ORG_ADMIN:
        messages.error(request, 'Only organisation admins can manage locations.')
        return redirect('accounts:location_list')
    org = profile.organisation
    if not org:
        messages.error(request, 'Create or join an organisation first.')
        return redirect('accounts:profile')
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            loc = form.save(commit=False)
            loc.organisation = org
            loc.save()
            messages.success(request, 'Location created.')
            return redirect('accounts:location_list')
    else:
        form = LocationForm()
    return render(request, 'accounts/location_form.html', {'form': form, 'mode': 'Create'})

@login_required
def location_edit(request, pk):
    profile = request.user.profile
    if profile.role != profile.ROLE_ORG_ADMIN:
        messages.error(request, 'Only organisation admins can manage locations.')
        return redirect('accounts:location_list')
    org = profile.organisation
    location = get_object_or_404(Location, pk=pk, organisation=org)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated.')
            return redirect('accounts:location_list')
    else:
        form = LocationForm(instance=location)
    return render(request, 'accounts/location_form.html', {'form': form, 'mode': 'Edit'})
