from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Order, Pizza


class CartCheckoutTests(TestCase):
    def setUp(self):
        self.pizza = Pizza.objects.create(
            title='Test pizza',
            description='Test description',
            price=Decimal('450.00'),
        )

    def test_add_to_cart_stores_item_in_session(self):
        response = self.client.get(
            reverse('main:add_to_cart', args=('pizza', self.pizza.id)),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.client.session['cart'],
            {f'pizza_{self.pizza.id}': 1},
        )

    def test_checkout_creates_order_and_clears_cart(self):
        session = self.client.session
        session['cart'] = {f'pizza_{self.pizza.id}': 2}
        session.save()

        response = self.client.post(reverse('main:checkout'), data={
            'customer_name': 'Alex',
            'phone': '+79991234567',
            'address': 'Test street, 1',
            'comment': 'No onion',
        })

        order = Order.objects.get()
        self.assertRedirects(
            response,
            reverse('main:order_success', args=(order.id,)),
        )
        self.assertEqual(order.total_price, Decimal('900.00'))
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.get().quantity, 2)
        self.assertEqual(self.client.session['cart'], {})
