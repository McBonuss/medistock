from django import forms

from .models import StockItem, StockMovement

class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['product', 'qty_on_hand', 'reorder_threshold']

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'reason']

    def __init__(self, *args, stock_item=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock_item = stock_item

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise forms.ValidationError('Quantity must be a positive integer.')
        return qty

    def clean(self):
        cleaned = super().clean()
        movement_type = cleaned.get('movement_type')
        qty = cleaned.get('quantity')
        reason = (cleaned.get('reason') or '').strip()

        if movement_type == StockMovement.TYPE_ADJUST and not reason:
            self.add_error('reason', 'Adjustment requires a reason.')

        if self.stock_item and movement_type == StockMovement.TYPE_OUT and qty is not None:
            if qty > self.stock_item.qty_on_hand:
                self.add_error('quantity', 'Cannot use more than the quantity on hand.')

        return cleaned
