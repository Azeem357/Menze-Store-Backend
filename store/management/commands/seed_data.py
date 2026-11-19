from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Product, Order, OrderItem
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed 6 months of dummy orders data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Get or create test user
        user, _ = User.objects.get_or_create(
            username='testcustomer',
            defaults={'email': 'customer@menze.com'}
        )
        user.set_password('Test1234')
        user.save()

        # Get products
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Add products first in admin.'))
            return

        now = timezone.now()
        order_count = 0

        for days_ago in range(180, 0, -1):
            date = now - timedelta(days=days_ago)
            daily_orders = random.randint(1, 8)

            for _ in range(daily_orders):
                # Create order
                order = Order.objects.create(
                    user=user,
                    status=random.choice(['delivered', 'delivered', 'delivered', 'cancelled']),
                )

                # Manually update created_at after creation
                Order.objects.filter(pk=order.pk).update(created_at=date)

                # Add 1-3 items per order
                selected = random.sample(products, min(random.randint(1, 3), len(products)))
                for product in selected:
                    quantity = random.randint(1, 3)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )

                order.calculate_total()
                order_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Seeded {order_count} orders successfully!'))