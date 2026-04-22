from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from catalog.models import Category, Product
from .models import CartItem
from .utils import get_or_create_cart


User = get_user_model()


class CartQuantityValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cartuser", password="pass12345")
        self.client.login(username="cartuser", password="pass12345")
        category = Category.objects.create(name="Supplies", slug="supplies")
        self.product = Product.objects.create(
            category=category,
            name="Face Mask",
            sku="MASK-001",
            price_gbp="2.50",
        )

    def test_add_to_cart_rejects_non_numeric_quantity(self):
        response = self.client.post(
            reverse("cart:add_to_cart", kwargs={"product_pk": self.product.pk}),
            {"quantity": "abc"},
        )

        self.assertEqual(response.status_code, 302)
        item = CartItem.objects.get(product=self.product, cart__user=self.user)
        self.assertEqual(item.quantity, 1)

    def test_update_item_rejects_non_numeric_quantity(self):
        cart = get_or_create_cart(self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=4)

        response = self.client.post(
            reverse("cart:update_item", kwargs={"item_pk": item.pk}),
            {"quantity": "not-a-number"},
        )

        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 4)
