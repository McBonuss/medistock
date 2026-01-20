from django.contrib import admin
from .models import StockItem, StockMovement, ReceivedLot


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("location", "product", "qty_on_hand", "reorder_threshold")
    list_filter = ("location__organisation", "location")
    search_fields = ("location__name", "location__organisation__name", "product__name", "product__sku")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("stock_item", "movement_type", "quantity", "created_by", "created_at")
    list_filter = ("movement_type", "created_at")
    search_fields = ("stock_item__product__name", "stock_item__location__name", "created_by__username")


@admin.register(ReceivedLot)
class ReceivedLotAdmin(admin.ModelAdmin):
    list_display = ("location", "product", "lot_number", "expiry_date", "qty_received", "created_at")
    list_filter = ("expiry_date", "location")
    search_fields = ("lot_number", "product__name", "location__name")
