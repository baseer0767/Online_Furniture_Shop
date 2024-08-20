from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from about.models import Order

class Command(BaseCommand):
    help = 'Update order status from Pending to Done after 2 days'

    def handle(self, *args, **kwargs):
        two_days_ago = timezone.now() - timedelta(minutes=2)
        orders_to_update = Order.objects.filter(delivery_status='Pending', order_date__lte=two_days_ago)
        
        for order in orders_to_update:
            order.delivery_status = 'Done'
            order.save()
            self.stdout.write(self.style.SUCCESS(f'Order {order.order_id} status updated to Done'))
