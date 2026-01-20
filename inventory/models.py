from django.conf import settings
from django.db import models

from accounts.models import Location
from catalog.models import Product

class StockItem(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stock_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty_on_hand = models.PositiveIntegerField(default=0)
    reorder_threshold = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ('location', 'product')

    def __str__(self):
        return f"{self.location} — {self.product}"

    @property
    def is_low(self):
        return self.qty_on_hand <= self.reorder_threshold

class StockMovement(models.Model):
    TYPE_IN = 'IN'
    TYPE_OUT = 'OUT'
    TYPE_ADJUST = 'ADJ'
    TYPE_CHOICES = [
        (TYPE_IN, 'Restock'),
        (TYPE_OUT, 'Usage'),
        (TYPE_ADJUST, 'Adjustment'),
    ]

    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} ({self.stock_item})"

class ReceivedLot(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='received_lots')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lot_number = models.CharField(max_length=50)
    expiry_date = models.DateField(null=True, blank=True)
    qty_received = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lot {self.lot_number} — {self.product}"
