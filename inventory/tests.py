from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Organisation, Location, UserProfile
from catalog.models import Category, Product
from .forms import StockMovementForm
from .models import StockItem, StockMovement


User = get_user_model()


class InventoryAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        org = Organisation.objects.create(name="Test Org")
        Location.objects.create(organisation=org, name="Ward 1")
        self.user.profile.organisation = org
        self.user.profile.paid_access = False
        self.user.profile.save()

    def test_inventory_requires_paid_access(self):
        self.client.login(username="alice", password="pass12345")
        resp = self.client.get(reverse("inventory:dashboard"))
        self.assertEqual(resp.status_code, 302)


class StockMovementFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="pass12345")
        org = Organisation.objects.create(name="Clinic Org")
        loc = Location.objects.create(organisation=org, name="Clinic A")
        profile: UserProfile = self.user.profile
        profile.organisation = org
        profile.paid_access = True
        profile.save()

        cat = Category.objects.create(name="Gloves")
        product = Product.objects.create(category=cat, name="Nitrile Gloves", sku="GLV-001", price_gbp=9.99)
        self.stock_item = StockItem.objects.create(location=loc, product=product, qty_on_hand=10, reorder_threshold=3)

    def test_cannot_use_more_than_on_hand(self):
        form = StockMovementForm(data={
            "movement_type": StockMovement.TYPE_OUT,
            "quantity": 11,
            "reason": "",
        }, stock_item=self.stock_item)
        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)

    def test_adjust_requires_reason(self):
        form = StockMovementForm(data={
            "movement_type": StockMovement.TYPE_ADJUST,
            "quantity": 1,
            "reason": "",
        }, stock_item=self.stock_item)
        self.assertFalse(form.is_valid())
        self.assertIn("reason", form.errors)
