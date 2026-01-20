from django.contrib import admin
from .models import Organisation, Location, UserProfile


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "city", "postcode", "created_at")
    list_filter = ("organisation", "city")
    search_fields = ("name", "organisation__name", "postcode")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "paid_access")
    list_filter = ("role", "paid_access")
    search_fields = ("user__username", "organisation__name")
