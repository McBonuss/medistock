from django.conf import settings

def project_settings(request):
    """Expose a small safe subset of settings to templates."""
    return {
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        "DEBUG": settings.DEBUG,
    }
