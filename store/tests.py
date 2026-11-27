from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Order, OrderItem, Product


class OrderSyncViewTests(TestCase):
    def test_sync_includes_order_item_price_quantity_and_product(self):
        user = User.objects.create_user(username='customer')
        product = Product.objects.create(
            name='Test product',
            price='25.00',
            stock=0,
        )
        order = Order.objects.create(
            user=user,
            status='delivered',
            total_price='40.00',
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price='20.00',
        )

        response = APIClient().get('/api/orders/sync/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['items'], [{
            'product_id': product.id,
            'product_name': 'Test product',
            'quantity': 2,
            'price': '20.00',
        }])
