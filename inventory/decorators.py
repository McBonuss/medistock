from django.contrib import messages
from django.shortcuts import redirect


def paid_access_required(view_func):
    def _wrapped(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not profile or not profile.paid_access:
            messages.error(request, 'Inventory dashboard is available after a successful checkout.')
            return redirect('catalog:product_list')
        return view_func(request, *args, **kwargs)
    return _wrapped
