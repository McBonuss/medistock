from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    extra = 0
    readonly_fields = ("product", "quantity", "line_total_gbp")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "location", "status", "total_gbp", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "location__name", "stripe_session_id")
    inlines = (OrderLineItemInline,)


@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "line_total_gbp")
    search_fields = ("order__id", "product__name")
